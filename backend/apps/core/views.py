from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.tokens import default_token_generator
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils import timezone
from django.views.decorators.http import require_http_methods, require_POST

from apps.usuarios.models import Usuario
from .forms import DespesaForm
from .models import Despesa


def index(request):
    return redirect('dashboard' if request.user.is_authenticated else 'login')


def login_page(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    erro_login = ''
    if request.method == 'POST':
        usuario = request.POST.get('usuario', '').strip()
        senha = request.POST.get('senha', '')
        logins_por_email = list(
            Usuario.objects.filter(email__iexact=usuario)
            .values_list('login', flat=True)[:2]
        )
        if len(logins_por_email) == 1:
            usuario = logins_por_email[0]
            user = authenticate(request, username=usuario, password=senha)
        elif len(logins_por_email) > 1:
            user = None
        else:
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
def mais_opcoes(request):
    return render(request, 'estrela_modas/mais_opcoes.html')


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
