from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import redirect, render

from apps.estoque.models import MovimentacaoEstoque
from apps.produtos.models import Produto
from .forms import ItemVendaFormSet, VendaForm
from .models import ItemVenda, Venda


@login_required
def nova_venda(request):
    form = VendaForm(
        request.POST or None,
        initial={'cliente': request.GET.get('cliente')},
    )
    itens_formset = ItemVendaFormSet(request.POST or None, prefix='itens')
    if request.method == 'POST' and form.is_valid() and itens_formset.is_valid():
        dados = form.cleaned_data
        linhas = [linha.cleaned_data for linha in itens_formset.forms if linha.cleaned_data.get('produto')]
        if not linhas:
            form.add_error(None, 'Adicione pelo menos um produto à venda.')
        else:
            ids_produtos = {linha['produto'].pk for linha in linhas}
            with transaction.atomic():
                produtos = {
                    produto.pk: produto
                    for produto in Produto.objects.select_for_update().filter(pk__in=ids_produtos).order_by('pk')
                }
                quantidades = {}
                subtotal = Decimal('0.00')
                for linha in linhas:
                    produto = produtos[linha['produto'].pk]
                    quantidade = linha['quantidade']
                    quantidades[produto.pk] = quantidades.get(produto.pk, 0) + quantidade
                    subtotal += produto.preco_venda * quantidade

                for produto_id, total_quantidade in quantidades.items():
                    if produtos[produto_id].quantidade_estoque < total_quantidade:
                        for linha_form in itens_formset.forms:
                            if linha_form.cleaned_data.get('produto') and linha_form.cleaned_data['produto'].pk == produto_id:
                                linha_form.add_error('quantidade', 'Estoque insuficiente para a quantidade informada.')
                        break
                else:
                    if dados['desconto_aplicado'] > subtotal:
                        form.add_error('desconto_aplicado', 'O desconto não pode ser maior que o subtotal.')
                    else:
                        total = subtotal - dados['desconto_aplicado']
                        cliente = dados['cliente']
                        if not form.errors:
                            venda = Venda.objects.create(
                                cliente=cliente,
                                desconto_aplicado=dados['desconto_aplicado'],
                                valor_total=total,
                                forma_pagamento=dados['forma_pagamento'],
                            )
                            for linha in linhas:
                                produto = produtos[linha['produto'].pk]
                                quantidade = linha['quantidade']
                                ItemVenda.objects.create(
                                    venda=venda,
                                    produto=produto,
                                    quantidade=quantidade,
                                    preco_unitario=produto.preco_venda,
                                )
                            for produto_id, quantidade in quantidades.items():
                                produto = produtos[produto_id]
                                produto.quantidade_estoque -= quantidade
                                produto.save(update_fields=['quantidade_estoque'])
                                MovimentacaoEstoque.objects.create(
                                    produto=produto,
                                    tipo=MovimentacaoEstoque.Tipo.SAIDA,
                                    quantidade=quantidade,
                                    motivo=f'Saída da venda #{venda.pk}',
                                )
            if not form.errors and not any(item.errors for item in itens_formset.forms):
                messages.success(request, 'Venda registrada e estoque atualizado.')
                return redirect('nova_venda')

    return render(request, 'estrela_modas/nova_venda.html', {
        'form': form,
        'itens_formset': itens_formset,
        'vendas_recentes': Venda.objects.select_related('cliente')[:5],
    })
