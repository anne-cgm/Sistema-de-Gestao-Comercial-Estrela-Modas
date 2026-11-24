from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.tokens import default_token_generator
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.db import transaction
from django.db.models import F, Q, Sum
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils import timezone
from django.views.decorators.http import require_http_methods, require_POST
from decimal import Decimal

from .forms import (
    ClienteForm, CompraEntradaForm, DespesaForm, PagamentoDebitoForm,
    ItemVendaFormSet, ProdutoForm, TrocaForm, VendaForm,
)
from .models import (
    Cliente, Compra, Despesa, ItemCompra, ItemVenda, MovimentacaoEstoque,
    PagamentoDebito, Produto, Troca, Venda,
)
from usuarios.models import Usuario


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


@require_http_methods(['GET', 'POST'])
def recuperar_senha(request):
    if request.method == 'GET':
        return render(request, 'estrela_modas/recuperar_senha.html')

    email = request.POST.get('email', '').strip()
    usuarios_com_email = Usuario.objects.filter(email__iexact=email, is_active=True)
    administrador = usuarios_com_email.filter(is_superuser=True).first()
    mensagem = 'Se o endereço informado pertence a um administrador, o link de redefinição foi enviado.'
    tipo_mensagem = 'info'

    if administrador:
        uid = urlsafe_base64_encode(force_bytes(administrador.pk))
        token = default_token_generator.make_token(administrador)
        caminho = reverse('redefinir_senha', kwargs={'uidb64': uid, 'token': token})
        link = request.build_absolute_uri(caminho)
        try:
            send_mail(
                'Redefinição de senha — Estrela Modas',
                f'Olá, {administrador.nome}.\n\n'
                f'Use este link para cadastrar uma nova senha:\n{link}\n\n'
                'Se você não solicitou esta alteração, ignore esta mensagem.',
                None,
                [administrador.email],
            )
        except Exception:
            mensagem = 'Não foi possível enviar o e-mail agora. Confira a configuração de e-mail e tente novamente.'
            tipo_mensagem = 'error'
        else:
            mensagem = 'Se o endereço informado pertence a um administrador, o link de redefinição foi enviado.'
            tipo_mensagem = 'success'
    elif usuarios_com_email.exists():
        mensagem = 'Funcionário: consulte o administrador da loja para redefinir sua senha.'

    return render(request, 'estrela_modas/recuperar_senha.html', {
        'mensagem': mensagem,
        'tipo_mensagem': tipo_mensagem,
    })


def redefinir_senha(request, uidb64, token):
    administrador = None
    try:
        pk = force_str(urlsafe_base64_decode(uidb64))
        administrador = Usuario.objects.get(pk=pk, is_superuser=True, is_active=True)
    except (TypeError, ValueError, OverflowError, UnicodeDecodeError, Usuario.DoesNotExist):
        pass

    token_valido = administrador is not None and default_token_generator.check_token(administrador, token)
    erros = []
    if request.method == 'POST' and token_valido:
        senha = request.POST.get('senha', '')
        confirmacao = request.POST.get('confirmacao', '')
        if senha != confirmacao:
            erros.append('As senhas informadas não são iguais.')
        else:
            try:
                validate_password(senha, administrador)
            except ValidationError as exc:
                erros.extend(exc.messages)
            else:
                administrador.set_password(senha)
                administrador.save(update_fields=['password'])
                messages.success(request, 'Senha redefinida. Entre com sua nova senha.')
                return redirect('login')

    return render(request, 'estrela_modas/redefinir_senha.html', {
        'token_valido': token_valido,
        'erros': erros,
    })


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
            # Busca novamente a venda e bloqueia sua linha durante a transação.
            venda = Venda.objects.select_for_update().get(
                pk=dados['venda'].pk
            )

            # Confere o saldo atualizado antes de registrar o pagamento.
            if venda.forma_pagamento != Venda.FormaPagamento.FIADO:
                form.add_error('venda', 'Selecione uma venda fiada.')
            
            elif venda.saldo_devedor <= 0:
                form.add_error('venda', 'Essa dívida já está quitada.')

            elif dados['valor'] > venda.saldo_devedor:
                form.add_error(
                    'valor',
                    'O débito foi alterado; informe um valor até o saldo atual.'
                )
            else:
                PagamentoDebito.objects.create(
                    venda=venda,
                    valor=dados['valor'],
                    observacoes=dados['observacoes'],
                )

        if not form.errors:
            messages.success(request, 'Pagamento registrado.')
            return redirect('debitos')

    # Busca somente as vendas fiadas que ainda possuem saldo.
    venda_com_debito = [
        venda for venda in Venda.objects.filter(
            forma_pagamento=Venda.FormaPagamento.FIADO
        ).select_related('cliente')
        if venda.saldo_devedor > 0
    ]

    # Soma os saldos individuais das vendas.
    total_pendente = sum(
        (venda.saldo_devedor for venda in venda_com_debito),
        start=0
    )

    # Busca os últimos pagamentos e suas respectivas vendas e clientes.
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
    return render(request, 'estrela_modas/trocas.html', {
        'form': form,
        'registros': Troca.objects.select_related('produto_devolvido', 'produto_entregue')[:8],
    })


@login_required
def usuarios(request):
    if not request.user.is_superuser:
        return redirect('mais_opcoes')
    return render(request, 'estrela_modas/usuarios.html', {
        'usuarios': Usuario.objects.all(),
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
