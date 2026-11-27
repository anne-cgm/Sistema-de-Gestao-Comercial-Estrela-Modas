from datetime import timedelta
from decimal import Decimal

from django.contrib.auth.decorators import login_required
from django.db.models import DecimalField, ExpressionWrapper, F, Sum, Value
from django.db.models.functions import Coalesce, ExtractHour, TruncDate
from django.shortcuts import render
from django.utils import timezone

from apps.core.models import Despesa
from apps.estoque.models import Compra
from apps.produtos.models import Produto
from apps.usuarios.permissoes import exigir_permissao
from apps.vendas.models import ItemVenda, Venda

@login_required
@exigir_permissao('dashboard')
def dashboard(request):
    """Monta os indicadores da tela inicial a partir dos registros do banco."""
    hoje = timezone.localdate()

    # Aceita apenas os três períodos disponíveis na interface; para qualquer
    # valor inesperado, mantém o padrão dos últimos sete dias.
    periodo = request.GET.get('periodo', 'semana')
    if periodo not in {'hoje', 'semana', 'mes'}:
        periodo = 'semana'

    # Define os limites das consultas e os intervalos que serão desenhados.
    # A loja funciona das 09h às 19h; cada barra de hoje cobre uma hora aberta.
    if periodo == 'hoje':
        inicio_periodo = hoje
        rotulo_periodo = 'hoje'
        intervalos = []
    elif periodo == 'mes':
        inicio_periodo = hoje.replace(day=1)
        rotulo_periodo = 'neste mês'
        intervalos = []
        inicio_dia = 1
        while inicio_dia <= hoje.day:
            fim_dia = min(inicio_dia + 6, hoje.day)
            intervalos.append((
                hoje.replace(day=inicio_dia),
                hoje.replace(day=fim_dia),
                f'{inicio_dia}–{fim_dia}',
            ))
            inicio_dia = fim_dia + 1
    else:
        inicio_periodo = hoje - timedelta(days=6)
        rotulo_periodo = 'nos últimos 7 dias'
        nomes_dias = ('Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb', 'Dom')
        intervalos = [
            (dia, dia, nomes_dias[dia.weekday()])
            for dia in (inicio_periodo + timedelta(days=offset) for offset in range(7))
        ]

    # Reutiliza a mesma seleção de vendas nos totais, gráficos e pagamentos.
    vendas_periodo = Venda.objects.filter(
        data_venda__date__range=(inicio_periodo, hoje),
    )
    resumo_vendas = vendas_periodo.aggregate(total=Sum('valor_total'))
    total_vendas_periodo = resumo_vendas['total'] or 0
    quantidade_vendas_periodo = vendas_periodo.count()
    ticket_medio = (
        total_vendas_periodo / quantidade_vendas_periodo
        if quantidade_vendas_periodo else 0
    )

    # As despesas acompanham o mesmo intervalo das vendas selecionadas.
    despesas_periodo = Despesa.objects.filter(
        data_despesa__range=(inicio_periodo, hoje),
    )
    total_despesas_periodo = despesas_periodo.aggregate(total=Sum('valor_despesa'))['total'] or Decimal('0.00')
    quantidade_despesas_periodo = despesas_periodo.count()

    # O sistema não guarda o custo histórico em cada item vendido. Por isso,
    # este lucro é estimado usando o custo atual cadastrado no produto.
    custo_estimado = ItemVenda.objects.filter(
        venda__data_venda__date__range=(inicio_periodo, hoje),
    ).aggregate(
        total=Sum(ExpressionWrapper(
            F('quantidade') * F('produto__preco_custo'),
            output_field=DecimalField(max_digits=14, decimal_places=2),
        )),
    )['total'] or Decimal('0.00')
    lucro_estimado = total_vendas_periodo - custo_estimado

    # Agrupa as vendas por hora hoje e por dia/semana no restante dos períodos.
    if periodo == 'hoje':
        totais_por_hora = {
            linha['hora']: linha['total']
            for linha in (
                vendas_periodo
                .annotate(hora=ExtractHour('data_venda'))
                .values('hora')
                .annotate(total=Sum('valor_total'))
            )
        }
        valores_intervalos = [
            {
                'rotulo': f'{hora:02}–{hora + 1:02}h',
                'total': totais_por_hora.get(hora, Decimal('0.00')),
            }
            for hora in range(9, 19)
        ]
    else:
        totais_por_dia = {
            linha['dia']: linha['total']
            for linha in (
                vendas_periodo
                .annotate(dia=TruncDate('data_venda'))
                .values('dia')
                .annotate(total=Sum('valor_total'))
            )
        }
        valores_intervalos = [
            {
                'rotulo': rotulo,
                'total': sum(
                    (total for dia, total in totais_por_dia.items() if inicio <= dia <= fim),
                    Decimal('0.00'),
                ),
            }
            for inicio, fim, rotulo in intervalos
        ]
    # Converte os valores em alturas percentuais e destaca o intervalo de pico.
    maior_total = max((item['total'] for item in valores_intervalos), default=Decimal('0.00'))
    for item in valores_intervalos:
        item['altura'] = (
            max(10, round(item['total'] / maior_total * 100))
            if maior_total else 0
        )
        item['destaque'] = bool(maior_total and item['total'] == maior_total)

    pico_vendas = max(valores_intervalos, key=lambda item: item['total'], default=None)
    menor_movimento = min(valores_intervalos, key=lambda item: item['total'], default=None)
    if total_vendas_periodo:
        resumo_pico = f"Maior movimento: {pico_vendas['rotulo']} · R$ {pico_vendas['total']:.2f}"
        resumo_menor = f"Menor movimento: {menor_movimento['rotulo']} · R$ {menor_movimento['total']:.2f}"
    else:
        resumo_pico = 'Nenhuma venda no período'
        resumo_menor = ''

    # Soma o faturamento por modalidade e calcula sua participação no período.
    pagamentos_periodo = []
    for linha in vendas_periodo.values('forma_pagamento').annotate(total=Sum('valor_total')):
        pagamentos_periodo.append({
            'metodo': dict(Venda.FormaPagamento.choices)[linha['forma_pagamento']],
            'total': linha['total'],
            'percentual': round(linha['total'] / total_vendas_periodo * 100)
            if total_vendas_periodo else 0,
        })

    # O saldo fiado é um retrato atual, então não depende do filtro de período.
    # A anotação tem nome próprio para não conflitar com Venda.total_pago.
    vendas_fiadas = Venda.objects.filter(
        forma_pagamento=Venda.FormaPagamento.FIADO,
    ).annotate(
        total_pago_dashboard=Coalesce(
            Sum('pagamentos__valor'),
            Value(Decimal('0.00'), output_field=DecimalField(max_digits=12, decimal_places=2)),
        ),
    )
    saldo_fiado_pendente = Decimal('0.00')
    clientes_com_debito = set()
    for venda in vendas_fiadas:
        saldo = venda.valor_total - venda.total_pago_dashboard
        if saldo > 0:
            saldo_fiado_pendente += saldo
            if venda.cliente_id:
                clientes_com_debito.add(venda.cliente_id)

    # Estoque baixo representa a situação atual, independentemente do período.
    produtos_baixo = Produto.objects.filter(ativo=True, quantidade_estoque__lte=F('estoque_minimo'))

    # Classifica os produtos pela quantidade vendida no período selecionado.
    mais_vendidos = (
        ItemVenda.objects.filter(venda__data_venda__date__range=(inicio_periodo, hoje))
        .values('produto__nome_produto', 'produto__preco_venda')
        .annotate(unidades=Sum('quantidade'))
        .order_by('-unidades')[:3]
    )
    # Envia ao template os dados já calculados para renderização no servidor.
    return render(request, 'estrela_modas/dashboard.html', {
        'periodo': periodo,
        'rotulo_periodo': rotulo_periodo,
        'quantidade_vendas_periodo': quantidade_vendas_periodo,
        'total_vendas_periodo': total_vendas_periodo,
        'ticket_medio': ticket_medio,
        'lucro_estimado': lucro_estimado,
        'total_despesas_periodo': total_despesas_periodo,
        'quantidade_despesas_periodo': quantidade_despesas_periodo,
        'saldo_fiado_pendente': saldo_fiado_pendente,
        'clientes_com_debito': len(clientes_com_debito),
        'vendas_por_intervalo': valores_intervalos,
        'resumo_pico': resumo_pico,
        'resumo_menor': resumo_menor,
        'pagamentos_periodo': pagamentos_periodo,
        'quantidade_produtos': Produto.objects.filter(ativo=True).count(),
        'produtos_baixo': produtos_baixo[:5],
        'quantidade_estoque_baixo': produtos_baixo.count(),
        'mais_vendidos': mais_vendidos,
    })


@login_required
@exigir_permissao('relatorios')
def relatorios(request):
    """Monta os totais e listas usados na página de relatórios do mês atual."""
    hoje = timezone.localdate()
    vendas = Venda.objects.filter(data_venda__date__gte=hoje.replace(day=1))
    itens_mais_vendidos = (
        ItemVenda.objects.filter(venda__data_venda__date__gte=hoje.replace(day=1))
        .values('produto__nome_produto')
        .annotate(unidades=Sum('quantidade'))
        .order_by('-unidades')[:5]
    )
    produtos_baixo = Produto.objects.filter(ativo=True, quantidade_estoque__lte=F('estoque_minimo'))
    return render(request, 'estrela_modas/relatorios.html', {
        'total_vendas': vendas.aggregate(total=Sum('valor_total'))['total'] or 0,
        'quantidade_vendas': vendas.count(),
        'mais_vendidos': itens_mais_vendidos,
        'produtos_baixo': produtos_baixo,
        'total_despesas': Despesa.objects.filter(data_despesa__gte=hoje.replace(day=1)).aggregate(total=Sum('valor_despesa'))['total'] or 0,
        'total_compras': Compra.objects.filter(data_chegada__date__gte=hoje.replace(day=1)).aggregate(total=Sum('valor_total'))['total'] or 0,
    })
