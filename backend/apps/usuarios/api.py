import json
import re
import unicodedata
from functools import wraps

from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

from .models import ConfiguracaoPermissoesFuncionarios, Usuario


PERMISSOES_DISPONIVEIS = {
    'dashboard', 'produtos', 'estoque', 'vendas', 'clientes', 'relatorios',
}


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
    return {
        'id': usuario.pk,
        'nome': usuario.nome,
        'login': usuario.login,
        'email': usuario.email,
        'perfil': 'administrador' if usuario.is_superuser else 'funcionario',
        'ativo': usuario.is_active and usuario.ativo,
    }


def _login_disponivel(email):
    """Gera login único a partir do e-mail, pois o formulário não pede login."""
    base = unicodedata.normalize('NFKD', email.split('@', 1)[0])
    base = ''.join(letra for letra in base if not unicodedata.combining(letra))
    base = re.sub(r'[^a-zA-Z0-9._-]+', '.', base).strip('._-')[:90] or 'funcionario'
    login = base
    sufixo = 2
    while Usuario.objects.filter(login__iexact=login).exists():
        final = f'.{sufixo}'
        login = f'{base[:100 - len(final)]}{final}'
        sufixo += 1
    return login


def _validar_usuario(dados, usuario=None):
    erros = {}
    nome = str(dados.get('nome', '')).strip()
    email = str(dados.get('email', '')).strip().lower()
    perfil = dados.get('perfil', 'funcionario')
    status = dados.get('ativo', 'sim')
    senha = str(dados.get('novaSenha', ''))
    confirmacao = str(dados.get('confirmarSenha', ''))

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

    usuario = Usuario.objects.create_user(
        login=_login_disponivel(validacao['email']),
        email=validacao['email'],
        password=validacao['senha'],
        nome=validacao['nome'],
        is_superuser=validacao['perfil'] == 'administrador',
        is_staff=validacao['perfil'] == 'administrador',
        is_active=validacao['ativo'],
        ativo=validacao['ativo'],
    )
    return JsonResponse({'usuario': _serializar_usuario(usuario)}, status=201)


@require_http_methods(['PATCH'])
@_administrador_api
def api_usuario_detalhe(request, pk):
    try:
        usuario = Usuario.objects.get(pk=pk)
    except Usuario.DoesNotExist:
        return JsonResponse({'erro': 'Usuário não encontrado.'}, status=404)

    dados = _ler_json(request)
    if dados is None:
        return JsonResponse({'erro': 'O corpo da solicitação precisa ser um JSON válido.'}, status=400)
    validacao = _validar_usuario(dados, usuario)
    if validacao['erros']:
        return JsonResponse({'erros': validacao['erros']}, status=400)

    if usuario.pk == request.user.pk and not validacao['ativo']:
        return JsonResponse({'erro': 'Você não pode desativar sua própria conta.'}, status=400)

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
    configuracao, _ = ConfiguracaoPermissoesFuncionarios.objects.get_or_create(pk=1)
    if request.method == 'GET':
        return JsonResponse({'permissoes': configuracao.permissoes})

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
