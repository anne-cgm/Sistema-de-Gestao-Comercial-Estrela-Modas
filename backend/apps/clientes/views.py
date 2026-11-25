from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from apps.vendas.models import Venda
from .forms import ClienteForm, PagamentoDebitoForm
from .models import Cliente, PagamentoDebito


@login_required
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
            Q(nome_cliente__icontains=busca) | Q(telefone__icontains=busca) | Q(cpf_cliente__icontains=busca)
        )
    return render(request, 'estrela_modas/clientes.html', {
        'form': form,
        'clientes': lista_clientes,
    })


@login_required
def cliente_detalhes(request, pk):
    cliente = get_object_or_404(
        Cliente.objects.prefetch_related(
            'vendas__itens__produto',
            'vendas__pagamentos',
        ),
        pk=pk,
    )

    if request.method == 'POST':
        nome = request.POST.get('nome_cliente', '').strip()
        telefone = request.POST.get('telefone', '').strip()
        if not nome:
            form_error = 'Informe o nome completo do cliente.'
        else:
            cliente.nome_cliente = nome
            cliente.telefone = telefone
            cliente.save(update_fields=['nome_cliente', 'telefone'])
            messages.success(request, 'Dados do cliente atualizados com sucesso.')
            return redirect('cliente_detalhes', pk=cliente.pk)
    else:
        form_error = ''

    vendas = list(cliente.vendas.all())
    compras = [venda for venda in vendas if venda.itens.exists()]
    vendas_fiadas = [venda for venda in vendas if venda.forma_pagamento == Venda.FormaPagamento.FIADO]
    credito_disponivel = max(cliente.limite_credito - cliente.saldo_devedor, Decimal('0.00'))

    return render(request, 'estrela_modas/cliente-detalhes.html', {
        'cliente': cliente,
        'compras': compras,
        'vendas_fiadas': vendas_fiadas,
        'saldo_devedor': cliente.saldo_devedor,
        'credito_disponivel': credito_disponivel,
        'form_error': form_error,
    })


def novo_cliente(request):
    form = ClienteForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Cliente cadastrado com sucesso.')
        return redirect('clientes')
    return render(request, 'estrela_modas/novo_cliente.html', {'form': form})


@login_required
def debitos(request):
    form = PagamentoDebitoForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        dados = form.cleaned_data
        with transaction.atomic():
            venda = Venda.objects.select_for_update().get(pk=dados['venda'].pk)
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

    venda_com_debito = [
        venda for venda in Venda.objects.filter(
            forma_pagamento=Venda.FormaPagamento.FIADO
        ).select_related('cliente')
        if venda.saldo_devedor > 0
    ]
    total_pendente = sum(
        (venda.saldo_devedor for venda in venda_com_debito),
        start=0,
    )
    pagamentos_recentes = (
        PagamentoDebito.objects
        .select_related('venda', 'venda__cliente')
        .order_by('-data_pagamento')[:8]
    )
    return render(request, 'estrela_modas/debitos.html', {
        'form': form,
        'vendas_com_debito': venda_com_debito,
        'total_pendente': total_pendente,
        'pagamentos_recentes': pagamentos_recentes,
    })
