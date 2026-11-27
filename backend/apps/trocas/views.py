from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import render

from apps.estoque.models import MovimentacaoEstoque
from apps.produtos.models import Produto
from apps.vendas.models import Venda
from apps.usuarios.permissoes import exigir_permissao
from .forms import TrocaForm
from .models import Troca


@login_required
@exigir_permissao('trocas')
def trocas(request):
    form = TrocaForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        dados = form.cleaned_data
        try:
            with transaction.atomic():
                devolvido = Produto.objects.select_for_update().get(pk=dados['produto_devolvido'].pk)
                entregue = None
                if dados['produto_entregue']:
                    entregue = Produto.objects.select_for_update().get(pk=dados['produto_entregue'].pk)
                    if entregue.quantidade_estoque < 1:
                        form.add_error('produto_entregue', 'Não há estoque disponível do produto escolhido.')
                        raise ValueError('estoque')
                troca = form.save()
                devolvido.quantidade_estoque += 1
                devolvido.save(update_fields=['quantidade_estoque'])
                MovimentacaoEstoque.objects.create(
                    produto=devolvido,
                    tipo=MovimentacaoEstoque.Tipo.ENTRADA,
                    quantidade=1,
                    motivo=f'Devolução da troca #{troca.pk}',
                )
                if entregue:
                    entregue.quantidade_estoque -= 1
                    entregue.save(update_fields=['quantidade_estoque'])
                    MovimentacaoEstoque.objects.create(
                        produto=entregue,
                        tipo=MovimentacaoEstoque.Tipo.SAIDA,
                        quantidade=1,
                        motivo=f'Produto entregue na troca #{troca.pk}',
                    )
        except ValueError:
            pass
        else:
            messages.success(request, 'Troca registrada e estoque atualizado.')
            return redirect('trocas')
    return render(request, 'estrela_modas/trocas.html', {
        'form': form,
        'registros': Troca.objects.select_related('produto_devolvido', 'produto_entregue')[:8],
    })
