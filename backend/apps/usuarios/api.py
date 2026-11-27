import json
import re
import secrets
from functools import wraps
from datetime import timedelta

from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.db import transaction
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.http import require_http_methods

from .models import ConfiguracaoPermissoesFuncionarios, Usuario
from .permissoes import PAGINAS_PERMITIDAS, PERMISSOES_DISPONIVEIS, permissoes_ativas_do_funcionario


def _administrador_api(view):
    """Restringe estas rotas a administradores e devolve erros em JSON."""
    @wraps(view)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({'erro': 'É necessário entrar no sistema.'}, status=401)
        if not request.user.is_superuser:
            return JsonResponse({'erro': 'Apenas administradores podem gerenciar usuários.'}, status=403)
        return view(request, *args, **kwargs)
    return wrapper


def _ler_json(request):
    try:
        dados = json.loads(request.body or '{}')
    except (json.JSONDecodeError, UnicodeDecodeError):
        return None
    return dados if isinstance(dados, dict) else None


def _serializar_usuario(usuario):
    """Converte o perfil em dados seguros para a interface administrativa."""
    return {
        'id': usuario.pk,
        'nome': usuario.nome,
        'login': usuario.login,
        'email': usuario.email,
        'perfil': 'administrador' if usuario.is_superuser else 'funcionario',
        'ativo': usuario.is_active and usuario.ativo,
        'codigo_recuperacao_configurado': bool(
            usuario.codigo_recuperacao_hash
            and usuario.codigo_recuperacao_expira_em
            and usuario.codigo_recuperacao_expira_em > timezone.now()
        ),
        'codigo_recuperacao_expira_em': (
            usuario.codigo_recuperacao_expira_em.isoformat()
            if usuario.codigo_recuperacao_expira_em else None
        ),
    }


def _criar_codigo_recuperacao():
    """Retorna um código legível e sua validade de 24 horas."""
    alfabeto = 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789'
    blocos = [
        ''.join(secrets.choice(alfabeto) for _ in range(4))
        for _ in range(3)
    ]
    return '-'.join(blocos), timezone.now() + timedelta(hours=24)


def _validar_usuario(dados, usuario=None):
    erros = {}
    login = str(dados.get('login', '')).strip()
    nome = str(dados.get('nome', '')).strip()
    email = str(dados.get('email', '')).strip().lower()
    perfil = dados.get('perfil', 'funcionario')
    status = dados.get('ativo', 'sim')
    senha = str(dados.get('novaSenha', ''))
    confirmacao = str(dados.get('confirmarSenha', ''))

    # O login identifica a conta e precisa ser único, curto e sem espaços.
    if not login:
        erros['login'] = 'Informe o login.'
    elif len(login) > 100 or not re.fullmatch(r'[A-Za-z0-9._-]+', login):
        erros['login'] = 'Use até 100 caracteres: letras sem acento, números, ponto, hífen ou sublinhado.'
    else:
        login_repetido = Usuario.objects.filter(login__iexact=login)
        if usuario:
            login_repetido = login_repetido.exclude(pk=usuario.pk)
        if login_repetido.exists():
            erros['login'] = 'Este login já está cadastrado.'
    if not nome:
        erros['nome'] = 'Informe o nome.'
    if not email:
        erros['email'] = 'Informe o e-mail.'
    else:
        try:
            validate_email(email)
        except ValidationError:
            erros['email'] = 'Informe um e-mail válido.'
        else:
            repetido = Usuario.objects.filter(email__iexact=email)
            if usuario:
                repetido = repetido.exclude(pk=usuario.pk)
            if repetido.exists():
                erros['email'] = 'Este e-mail já está cadastrado.'
    if perfil not in {'administrador', 'funcionario'}:
        erros['perfil'] = 'Perfil inválido.'
    if status not in {'sim', 'nao'}:
        erros['ativo'] = 'Status inválido.'
    if not usuario and not senha:
        erros['novaSenha'] = 'Informe uma senha para o novo usuário.'
    if senha or confirmacao:
        if senha != confirmacao:
            erros['confirmarSenha'] = 'As senhas informadas não são iguais.'
        elif senha:
            try:
                validate_password(senha, usuario)
            except ValidationError as exc:
                erros['novaSenha'] = exc.messages

    return {
        'erros': erros,
        'login': login,
        'nome': nome,
        'email': email,
        'perfil': perfil,
        'ativo': status == 'sim',
        'senha': senha,
    }


@require_http_methods(['GET', 'POST'])
@_administrador_api
def api_usuarios(request):
    if request.method == 'GET':
        usuarios = Usuario.objects.order_by('nome', 'login')
        return JsonResponse({'usuarios': [_serializar_usuario(usuario) for usuario in usuarios]})

    dados = _ler_json(request)
    if dados is None:
        return JsonResponse({'erro': 'O corpo da solicitação precisa ser um JSON válido.'}, status=400)
    validacao = _validar_usuario(dados)
    if validacao['erros']:
        return JsonResponse({'erros': validacao['erros']}, status=400)

    # Contas ativas já recebem um código temporário; contas inativas não podem usá-lo.
    codigo_recuperacao, expiracao_codigo = (
        _criar_codigo_recuperacao() if validacao['ativo'] else (None, None)
    )
    usuario = Usuario.objects.create_user(
        login=validacao['login'],
        email=validacao['email'],
        password=validacao['senha'],
        nome=validacao['nome'],
        is_superuser=validacao['perfil'] == 'administrador',
        is_staff=validacao['perfil'] == 'administrador',
        is_active=validacao['ativo'],
        ativo=validacao['ativo'],
        codigo_recuperacao_hash=make_password(codigo_recuperacao) if codigo_recuperacao else '',
        codigo_recuperacao_expira_em=expiracao_codigo,
    )
    resposta = JsonResponse({
        'usuario': _serializar_usuario(usuario),
        'codigo_recuperacao': codigo_recuperacao,
        'expira_em': expiracao_codigo.isoformat() if expiracao_codigo else None,
    }, status=201)
    resposta['Cache-Control'] = 'no-store'
    return resposta


@require_http_methods(['PATCH', 'DELETE'])
@_administrador_api
def api_usuario_detalhe(request, pk):
    try:
        usuario = Usuario.objects.get(pk=pk)
    except Usuario.DoesNotExist:
        return JsonResponse({'erro': 'Usuário não encontrado.'}, status=404)
    if not usuario.is_active or not usuario.ativo:
        return JsonResponse({'erro': 'Ative o usuário antes de gerar um código de recuperação.'}, status=400)

    # Impede que a sessão administrativa atual seja removida pela própria conta.
    if request.method == 'DELETE':
        if usuario.pk == request.user.pk:
            return JsonResponse({'erro': 'Você não pode excluir o usuário conectado.'}, status=400)

        login_excluido = usuario.login
        usuario.delete()
        return JsonResponse({'excluido': True, 'login': login_excluido})

    dados = _ler_json(request)
    if dados is None:
        return JsonResponse({'erro': 'O corpo da solicitação precisa ser um JSON válido.'}, status=400)
    validacao = _validar_usuario(dados, usuario)
    if validacao['erros']:
        return JsonResponse({'erros': validacao['erros']}, status=400)

    if usuario.pk == request.user.pk and not validacao['ativo']:
        return JsonResponse({'erro': 'Você não pode desativar sua própria conta.'}, status=400)
    if usuario.pk == request.user.pk and validacao['perfil'] != 'administrador':
        return JsonResponse({'erro': 'Você não pode remover seu próprio acesso de administrador.'}, status=400)

    usuario.login = validacao['login']
    usuario.nome = validacao['nome']
    usuario.email = validacao['email']
    usuario.ativo = validacao['ativo']
    usuario.is_active = validacao['ativo']
    usuario.is_superuser = validacao['perfil'] == 'administrador'
    usuario.is_staff = usuario.is_superuser
    if validacao['senha']:
        usuario.set_password(validacao['senha'])
    usuario.save()
    return JsonResponse({'usuario': _serializar_usuario(usuario)})


@require_http_methods(['GET', 'PUT'])
@_administrador_api
def api_permissoes_funcionarios(request):
    # Guarda uma única configuração compartilhada entre todas as contas de funcionário.
    configuracao, _ = ConfiguracaoPermissoesFuncionarios.objects.get_or_create(pk=1)
    if request.method == 'GET':
        return JsonResponse({
            'permissoes': configuracao.permissoes,
            'opcoes': PAGINAS_PERMITIDAS,
        })

    dados = _ler_json(request)
    permissoes = dados.get('permissoes') if dados else None
    if not isinstance(permissoes, list) or any(not isinstance(item, str) for item in permissoes):
        return JsonResponse({'erro': 'Envie uma lista de permissões válida.'}, status=400)
    desconhecidas = sorted(set(permissoes) - PERMISSOES_DISPONIVEIS)
    if desconhecidas:
        return JsonResponse({'erro': 'Há permissões desconhecidas.', 'itens': desconhecidas}, status=400)

    configuracao.permissoes = sorted(set(permissoes))
    configuracao.save(update_fields=['permissoes', 'atualizado_em'])
    return JsonResponse({'permissoes': configuracao.permissoes})


@login_required
def api_acesso_atual(request):
    """Fornece ao JavaScript o perfil e as permissões da sessão autenticada."""
    administrador = request.user.is_superuser
    permissoes = (
        sorted(PERMISSOES_DISPONIVEIS)
        if administrador
        else sorted(permissoes_ativas_do_funcionario())
    )
    return JsonResponse({
        'perfil': 'administrador' if administrador else 'funcionario',
        'permissoes': permissoes,
    })


@require_http_methods(['POST'])
@_administrador_api
def api_gerar_codigo_recuperacao(request, pk):
    """Gera ou substitui o código de recuperação de uma conta, sem armazená-lo em texto puro."""
    try:
        usuario = Usuario.objects.get(pk=pk)
    except Usuario.DoesNotExist:
        return JsonResponse({'erro': 'Usuário não encontrado.'}, status=404)

    # A geração manual substitui qualquer código ativo anterior.
    codigo, expiracao = _criar_codigo_recuperacao()

    # Só o hash e a validade ficam no banco; o código em texto é retornado uma vez.
    usuario.codigo_recuperacao_hash = make_password(codigo)
    usuario.codigo_recuperacao_expira_em = expiracao
    usuario.save(update_fields=['codigo_recuperacao_hash', 'codigo_recuperacao_expira_em'])
    resposta = JsonResponse({
        'codigo': codigo,
        'expira_em': expiracao.isoformat(),
    })
    resposta['Cache-Control'] = 'no-store'
    return resposta


@require_http_methods(['POST'])
def api_recuperar_senha_com_codigo(request):
    """Redefine a senha com e-mail e código temporário válido de qualquer perfil ativo."""
    dados = _ler_json(request)
    if dados is None:
        return JsonResponse({'erro': 'Solicitação inválida.'}, status=400)

    email = str(dados.get('email', '')).strip().lower()
    codigo = str(dados.get('codigo', '')).strip().upper()
    senha = str(dados.get('senha', ''))
    confirmacao = str(dados.get('confirmacao', ''))

    if not email or not codigo or not senha or not confirmacao:
        return JsonResponse({'erro': 'Preencha e-mail, código e os dois campos de senha.'}, status=400)
    if senha != confirmacao:
        return JsonResponse({'erro': 'As senhas informadas não são iguais.'}, status=400)

    with transaction.atomic():
        # O bloqueio impede que duas solicitações simultâneas usem o mesmo código.
        usuario = (
            Usuario.objects.select_for_update()
            .filter(email__iexact=email, is_active=True, ativo=True)
            .first()
        )
        codigo_valido = bool(
            usuario
            and usuario.codigo_recuperacao_hash
            and usuario.codigo_recuperacao_expira_em
            and usuario.codigo_recuperacao_expira_em > timezone.now()
            and check_password(codigo, usuario.codigo_recuperacao_hash)
        )
        if not codigo_valido:
            return JsonResponse({'erro': 'E-mail ou código inválido ou expirado. Peça ao administrador um código novo.'}, status=400)

        try:
            validate_password(senha, usuario)
        except ValidationError as erro:
            return JsonResponse({'erro': ' '.join(erro.messages)}, status=400)

        # O código é de uso único: a redefinição apaga o hash e a data de expiração.
        usuario.set_password(senha)
        usuario.codigo_recuperacao_hash = ''
        usuario.codigo_recuperacao_expira_em = None
        usuario.save(update_fields=[
            'password', 'codigo_recuperacao_hash', 'codigo_recuperacao_expira_em',
        ])
    return JsonResponse({'mensagem': 'Senha redefinida. Entre com a nova senha.'})
