from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import F, Q
from django.shortcuts import redirect, render

from apps.estoque.models import MovimentacaoEstoque
from apps.usuarios.permissoes import exigir_permissao
from .forms import ProdutoForm
from .models import Produto


@login_required
@exigir_permissao('produtos')
def produtos(request):
    busca = request.GET.get('q', '').strip()
    categoria = request.GET.get('categoria', '').strip()
    tamanho = request.GET.get('tamanho', '').strip()
    estoque_baixo = request.GET.get('estoque_baixo', '')

    lista_produtos = Produto.objects.filter(ativo=True)

    if busca:
        lista_produtos = lista_produtos.filter(
            Q(nome_produto__icontains=busca) | Q(sku__icontains=busca)
        )
    if categoria:
        lista_produtos = lista_produtos.filter(categoria__iexact=categoria)
    if tamanho:
        lista_produtos = lista_produtos.filter(tamanho__iexact=tamanho)
    if estoque_baixo == '1':
        lista_produtos = lista_produtos.filter(quantidade_estoque__lte=F('estoque_minimo'))

    categorias = Produto.objects.filter(ativo=True).exclude(categoria='').values_list('categoria', flat=True).distinct()
    tamanhos = Produto.objects.filter(ativo=True).exclude(tamanho='').values_list('tamanho', flat=True).distinct()

    return render(request, 'estrela_modas/produtos.html', {
        'produtos': lista_produtos,
        'termo_busca': busca,
        'categoria_selecionada': categoria,
        'tamanho_selecionado': tamanho,
        'estoque_baixo': estoque_baixo,
        'categorias': categorias,
        'tamanhos': tamanhos,
    })


@login_required
@exigir_permissao('produtos')
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
