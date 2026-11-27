from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import F, Q, Sum, Window
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from apps.usuarios.permissoes import exigir_permissao
from apps.vendas.models import Venda
from .forms import ClienteForm, PagamentoDebitoForm
from .models import Cliente, PagamentoDebito


def _cliente_detalhes_context(cliente, form_error=''):
    vendas = list(cliente.vendas.all())
    compras = [venda for venda in vendas if venda.itens.exists()]
    vendas_fiadas = [
        venda for venda in vendas
        if venda.forma_pagamento == Venda.FormaPagamento.FIADO
    ]
    return {
        'cliente': cliente,
        'compras': compras,
        'vendas_fiadas': vendas_fiadas,
        'saldo_devedor': cliente.saldo_devedor,
        'form_error': form_error,
    }


@login_required
@exigir_permissao('clientes')
def clientes(request):
    form = ClienteForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Cliente cadastrado com sucesso.')
        return redirect('clientes')
    busca = request.GET.get('q', '').strip()
    lista_clientes = Cliente.objects.all()
    if busca:
        lista_clientes = lista_clientes.filter(
            Q(nome_cliente__icontains=busca) | Q(telefone__icontains=busca)
        )
    return render(request, 'estrela_modas/clientes.html', {
        'form': form,
        'clientes': lista_clientes,
    })


@login_required
@exigir_permissao('clientes')
def cliente_detalhes(request, pk):
    cliente = get_object_or_404(
        Cliente.objects.prefetch_related(
            'vendas__itens__produto',
            'vendas__pagamentos',
        ),
        pk=pk,
    )

    form_error = ''
    if request.method == 'POST':
        nome = request.POST.get('nome_cliente', '').strip()
        telefone = request.POST.get('telefone', '').strip()
        if not nome:
            form_error = 'Informe o nome completo do cliente.'
        elif not telefone:
            form_error = 'Informe o telefone do cliente.'
        else:
            cliente.nome_cliente = nome
            cliente.telefone = telefone
            cliente.save(update_fields= ['nome_cliente', 'telefone'])
            messages.success(request, 'Dados do cliente atualizados com sucesso.')
            return redirect('cliente_detalhes', pk=cliente.pk)

    return render(
        request,
        'estrela_modas/cliente-detalhes.html',
        _cliente_detalhes_context(cliente, form_error),
    )


@login_required
@require_POST
@exigir_permissao('clientes')
def excluir_cliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if cliente.saldo_devedor > 0:
        return render(
            request,
            'estrela_modas/cliente-detalhes.html',
            _cliente_detalhes_context(
                cliente,
                'Não é possível excluir este cliente enquanto houver débitos pendentes.',
            ),
        )

    cliente.delete()
    messages.success(
        request,
        'Cliente excluído. O histórico de vendas e pagamentos foi preservado.',
    )
    return redirect('clientes')


@login_required
@exigir_permissao('clientes')
def novo_cliente(request):
    form = ClienteForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Cliente cadastrado com sucesso.')
        return redirect('clientes')
    return render(request, 'estrela_modas/novo_cliente.html', {'form': form})


@login_required
@exigir_permissao('debitos')
def debitos(request):
    form = PagamentoDebitoForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        dados = form.cleaned_data
        with transaction.atomic():
            # Busca novamente a venda e bloqueia linha durante a transação
            venda = Venda.objects.select_for_update().get(pk=dados['venda'].pk)

            # Confere o saldo atualizado antes de registrar o pagamento
            if venda.forma_pagamento != Venda.FormaPagamento.FIADO:
                form.add_error('venda', 'Selecione uma venda fiada.')
            elif venda.saldo_devedor <= 0:
                form.add_error('venda', 'Essa dívida já está quitada.')
            elif dados['valor'] > venda.saldo_devedor:
                form.add_error('valor', 'O débito foi alterado; informe um valor até o saldo atual.')
            else:
                PagamentoDebito.objects.create(
                    venda=venda,
                    valor=dados['valor'],
                    observacoes=dados['observacoes'],
                )
        if not form.errors:
            messages.success(request, 'Pagamento registrado.')
            return redirect('debitos')

    # Busca somente as vendas fiadas que ainda possuem saldo
    venda_com_debito = [
        venda for venda in Venda.objects.filter(
            forma_pagamento=Venda.FormaPagamento.FIADO
        ).select_related('cliente')
        if venda.saldo_devedor > 0
    ]

    # Soma os saldos individuais das vendas.
    total_pendente = sum(
        (venda.saldo_devedor for venda in venda_com_debito),
        start=0,
    )

    # Busca os últimos 8 pagamentos registrados, ordenados do mais recente para o mais antigo.
    pagamentos_recentes = (
        PagamentoDebito.objects
        .select_related('venda', 'venda__cliente')
        .annotate(
            total_pago_venda=Window(
                expression=Sum('valor'),
                partition_by=[F('venda_id')],
                order_by=[F('pk').asc()],
            ),
        )
        .annotate(
            saldo_restante=F('venda__valor_total') - F('total_pago_venda'),
        )
        .order_by('-pk')[:8]
    )
    return render(request, 'estrela_modas/debitos.html', {
        'form': form,
        'vendas_com_debito': venda_com_debito,
        'total_pendente': total_pendente,
        'pagamentos_recentes': pagamentos_recentes,
    })
