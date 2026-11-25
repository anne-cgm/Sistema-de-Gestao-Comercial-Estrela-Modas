from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import F
from django.shortcuts import redirect, render

from apps.produtos.models import Produto
from .forms import CompraEntradaForm
from .models import Compra, ItemCompra, MovimentacaoEstoque


@login_required
def estoque(request):
    return render(request, 'estrela_modas/estoque.html', {
        'produtos': Produto.objects.filter(ativo=True),
        'produtos_baixo': Produto.objects.filter(ativo=True, quantidade_estoque__lte=F('estoque_minimo')),
    })


@login_required
def compras(request):
    form = CompraEntradaForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        dados = form.cleaned_data
        with transaction.atomic():
            produto = Produto.objects.select_for_update().get(pk=dados['produto'].pk)
            quantidade = dados['quantidade']
            custo = dados['preco_custo_unitario']
            total = custo * quantidade
            compra = Compra.objects.create(
                fornecedor_nome=dados['fornecedor_nome'],
                numero_nota_fiscal=dados['numero_nota_fiscal'],
                valor_total=total,
            )
            ItemCompra.objects.create(
                compra=compra,
                produto=produto,
                quantidade=quantidade,
                preco_custo_unitario=custo,
            )
            produto.quantidade_estoque += quantidade
            produto.preco_custo = custo
            produto.save(update_fields=['quantidade_estoque', 'preco_custo'])
            MovimentacaoEstoque.objects.create(
                produto=produto,
                tipo=MovimentacaoEstoque.Tipo.ENTRADA,
                quantidade=quantidade,
                motivo=f'Entrada da compra #{compra.pk}',
            )
        messages.success(request, 'Compra registrada e estoque atualizado.')
        return redirect('compras')

    return render(request, 'estrela_modas/compras.html', {
        'form': form,
        'compras_recentes': Compra.objects.prefetch_related('itens__produto')[:5],
    })
