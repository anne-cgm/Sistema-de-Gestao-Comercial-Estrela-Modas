from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import F
from django.shortcuts import redirect, render

from apps.produtos.models import Produto
from apps.usuarios.permissoes import exigir_permissao
from .forms import CompraEntradaForm
from .models import Compra, ItemCompra, MovimentacaoEstoque


@login_required
@exigir_permissao('estoque')
def estoque(request):
    """Exibe os produtos ativos e os que precisam de reposição."""
    return render(request, 'estrela_modas/estoque.html', {
        'produtos': Produto.objects.filter(ativo=True),
        'produtos_baixo': Produto.objects.filter(ativo=True, quantidade_estoque__lte=F('estoque_minimo')),
    })


@login_required
@exigir_permissao('compras')
def compras(request):
    """Registra uma compra, cria a entrada de estoque e mostra as compras recentes."""
    # Um POST vazio também precisa manter o formulário vinculado para exibir erros.
    dados_enviados = request.POST if request.method == 'POST' else None
    form = CompraEntradaForm(dados_enviados)

    if request.method == 'POST' and form.is_valid():
        dados = form.cleaned_data
        try:
            # Mantém registro da compra, item, estoque e histórico como uma operação única.
            with transaction.atomic():
                # O bloqueio evita que duas entradas concorrentes percam atualização de estoque.
                produto = Produto.objects.select_for_update().get(
                    pk=dados['produto'].pk,
                    ativo=True,
                )
                quantidade = dados['quantidade']
                custo = dados['preco_custo_unitario']

                # Esta tela registra uma única variação por compra; seu total é custo × quantidade.
                compra = Compra.objects.create(
                    fornecedor_nome=dados['fornecedor_nome'],
                    numero_nota_fiscal=dados['numero_nota_fiscal'],
                    valor_total=custo * quantidade,
                )
                ItemCompra.objects.create(
                    compra=compra,
                    produto=produto,
                    quantidade=quantidade,
                    preco_custo_unitario=custo,
                )

                # Atualiza a quantidade disponível e o custo mais recente do produto.
                produto.quantidade_estoque += quantidade
                produto.preco_custo = custo
                produto.save(update_fields=['quantidade_estoque', 'preco_custo'])

                # Mantém um histórico explícito para auditoria das movimentações do estoque.
                MovimentacaoEstoque.objects.create(
                    produto=produto,
                    tipo=MovimentacaoEstoque.Tipo.ENTRADA,
                    quantidade=quantidade,
                    motivo=f'Entrada da compra #{compra.pk}',
                )
        except Produto.DoesNotExist:
            # O produto pode ter sido desativado entre a exibição e o envio do formulário.
            form.add_error('produto', 'Este produto não está mais ativo. Selecione outro produto.')
        else:
            # A confirmação só é exibida depois que a transação foi concluída.
            messages.success(request, 'Compra registrada e estoque atualizado.')
            return redirect('compras')

    # O prefetch carrega os itens associados às cinco compras exibidas na página.
    return render(request, 'estrela_modas/compras.html', {
        'form': form,
        'compras_recentes': Compra.objects.prefetch_related('itens__produto')[:5],
    })
