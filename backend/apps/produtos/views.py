from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Q
from django.shortcuts import redirect, render

from apps.estoque.models import MovimentacaoEstoque
from .forms import ProdutoForm
from .models import Produto


@login_required
def produtos(request):
    busca = request.GET.get('q', '').strip()
    lista_produtos = Produto.objects.filter(ativo=True)
    if busca:
        lista_produtos = lista_produtos.filter(Q(nome_produto__icontains=busca) | Q(sku__icontains=busca))
    return render(request, 'estrela_modas/produtos.html', {
        'produtos': lista_produtos,
        'termo_busca': busca,
    })


@login_required
def novo_produto(request):
    form = ProdutoForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        with transaction.atomic():
            produto = form.save()
            if produto.quantidade_estoque:
                MovimentacaoEstoque.objects.create(
                    produto=produto,
                    tipo=MovimentacaoEstoque.Tipo.ENTRADA,
                    quantidade=produto.quantidade_estoque,
                    motivo='Estoque inicial do cadastro',
                )
        messages.success(request, 'Produto cadastrado com sucesso.')
        return redirect('produtos')
    return render(request, 'estrela_modas/novo_produto.html', {'form': form})
