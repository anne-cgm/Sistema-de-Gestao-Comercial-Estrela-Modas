from django.contrib.auth.decorators import login_required
from django.db.models import F, Sum
from django.shortcuts import render
from django.utils import timezone

from apps.estoque.models import Compra
from apps.core.models import Despesa
from apps.produtos.models import Produto
from apps.vendas.models import ItemVenda, Venda


@login_required
def dashboard(request):
    hoje = timezone.localdate()
    vendas_hoje = Venda.objects.filter(data_venda__date=hoje)
    vendas_mes = Venda.objects.filter(data_venda__date__gte=hoje.replace(day=1))
    produtos_baixo = Produto.objects.filter(ativo=True, quantidade_estoque__lte=F('estoque_minimo'))
    mais_vendidos = (
        ItemVenda.objects.filter(venda__data_venda__date__gte=hoje.replace(day=1))
        .values('produto__nome_produto', 'produto__preco_venda')
        .annotate(unidades=Sum('quantidade'))
        .order_by('-unidades')[:3]
    )
    return render(request, 'estrela_modas/dashboard.html', {
        'quantidade_vendas_hoje': vendas_hoje.count(),
        'total_vendas_hoje': vendas_hoje.aggregate(total=Sum('valor_total'))['total'] or 0,
        'total_vendas_mes': vendas_mes.aggregate(total=Sum('valor_total'))['total'] or 0,
        'quantidade_produtos': Produto.objects.filter(ativo=True).count(),
        'produtos_baixo': produtos_baixo[:5],
        'quantidade_estoque_baixo': produtos_baixo.count(),
        'mais_vendidos': mais_vendidos,
    })


@login_required
def relatorios(request):
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
