from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import F, Q, Sum
from django.shortcuts import redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST
from decimal import Decimal

from .forms import (
    ClienteForm, CompraEntradaForm, DespesaForm, PagamentoDebitoForm,
    ItemVendaFormSet, ProdutoForm, TrocaForm, VendaForm,
)
from .models import (
    Cliente, Compra, Despesa, ItemCompra, ItemVenda, MovimentacaoEstoque,
    PagamentoDebito, Produto, Troca, Venda,
)


def index(request):
    return redirect('dashboard' if request.user.is_authenticated else 'login')


def login_page(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    erro_login = ''
    if request.method == 'POST':
        usuario = request.POST.get('usuario', '').strip()
        senha = request.POST.get('senha', '')
        user = authenticate(request, username=usuario, password=senha)
        if user is not None:
            auth_login(request, user)
            return redirect('dashboard')
        erro_login = 'Usuário ou senha inválidos.'
    return render(request, 'estrela_modas/login.html', {'erro_login': erro_login})


@require_POST
@login_required
def logout_page(request):
    auth_logout(request)
    return redirect('login')


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
def cadastro_produto(request):
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
    return render(request, 'estrela_modas/cadastro_produto.html', {'form': form})


@login_required
def estoque(request):
    return render(request, 'estrela_modas/estoque.html', {
        'produtos': Produto.objects.filter(ativo=True),
        'produtos_baixo': Produto.objects.filter(ativo=True, quantidade_estoque__lte=F('estoque_minimo')),
    })


@login_required
def nova_venda(request):
    form = VendaForm(request.POST or None)
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
                        if dados['forma_pagamento'] == Venda.FormaPagamento.FIADO:
                            cliente = Cliente.objects.select_for_update().get(pk=cliente.pk)
                            if cliente.limite_credito <= 0 or cliente.saldo_devedor + total > cliente.limite_credito:
                                form.add_error('cliente', 'O valor ultrapassa o limite de crédito disponível do cliente.')
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
def debitos(request):
    form = PagamentoDebitoForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        dados = form.cleaned_data
        with transaction.atomic():
            cliente = Cliente.objects.select_for_update().get(pk=dados['cliente'].pk)
            if dados['valor'] > cliente.saldo_devedor:
                form.add_error('valor', 'O débito foi alterado; informe um valor até o saldo atual.')
            else:
                PagamentoDebito.objects.create(
                    cliente=cliente,
                    valor=dados['valor'],
                    observacoes=dados['observacoes'],
                )
        if not form.errors:
            messages.success(request, 'Pagamento registrado.')
            return redirect('debitos')

    clientes_com_debito = [cliente for cliente in Cliente.objects.all() if cliente.saldo_devedor > 0]
    return render(request, 'estrela_modas/debitos.html', {
        'form': form,
        'clientes_com_debito': clientes_com_debito,
        'total_pendente': sum((cliente.saldo_devedor for cliente in clientes_com_debito), start=0),
        'pagamentos_recentes': PagamentoDebito.objects.select_related('cliente')[:8],
    })


@login_required
def mais_opcoes(request):
    return render(request, 'estrela_modas/mais_opcoes.html')


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


@login_required
def despesas(request):
    form = DespesaForm(request.POST or None, initial={'data_despesa': timezone.localdate()})
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Despesa registrada.')
        return redirect('despesas')
    return render(request, 'estrela_modas/registro.html', {
        'form': form,
        'titulo': 'Registrar despesa',
        'subtitulo': 'Lance os gastos operacionais da loja.',
        'registros': Despesa.objects.all()[:8],
        'tipo_registro': 'despesa',
    })


@login_required
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
    return render(request, 'estrela_modas/registro.html', {
        'form': form,
        'titulo': 'Registrar troca',
        'subtitulo': 'Registre o produto devolvido e a reposição, se houver.',
        'registros': Troca.objects.select_related('produto_devolvido', 'produto_entregue')[:8],
        'tipo_registro': 'troca',
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
