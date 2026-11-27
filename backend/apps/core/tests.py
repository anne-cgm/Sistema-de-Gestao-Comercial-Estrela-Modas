from django.contrib.auth import get_user_model
from django.contrib.staticfiles import finders
from django.test import TestCase
from django.urls import reverse

from apps.usuarios.models import ConfiguracaoPermissoesFuncionarios
from apps.usuarios.permissoes import PAGINAS_PERMITIDAS


# Classe de teste para verificar o redirecionamento e renderização de páginas
class PageRoutingTests(TestCase):

    # Prepara os dados necessários antes de cada teste, criando um usuário teste para autenticação.
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            login='teste',
            nome='Usuário de teste',
            email='teste@email.com',
            password='senha-teste-123'
        )
        ConfiguracaoPermissoesFuncionarios.objects.create(
            permissoes=[pagina['chave'] for pagina in PAGINAS_PERMITIDAS],
        )
    # Testa se a página inicial redireciona usuários não autenticados para a página de login.
    def test_home_redirects_anonymous_to_login(self):
        response = self.client.get(reverse('index'))

        self.assertRedirects(
            response,
            reverse('login'),
            fetch_redirect_response=False
        )
    # Teste para verificar se a página inicial redireciona usuários autenticados para o dashboard.
    def test_home_redirects_authenticated_to_dashboard(self):
        self.client.force_login(self.user)

        response = self.client.get(reverse('index'))

        self.assertRedirects(
            response,
            reverse('dashboard'),
            fetch_redirect_response=False
        )
    # Teste para verificar se a página de login é renderizada corretamente.
    def test_login_page_renders(self):
        response = self.client.get(reverse('login'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<form class="content stack login-form" method="post"')

    def test_login_accepts_email_and_password(self):
        response = self.client.post(reverse('login'), {
            'usuario': 'teste@email.com',
            'senha': 'senha-teste-123',
        })

        self.assertRedirects(response, reverse('dashboard'), fetch_redirect_response=False)

    def test_login_continues_accepting_username_and_password(self):
        response = self.client.post(reverse('login'), {
            'usuario': 'teste',
            'senha': 'senha-teste-123',
        })

        self.assertRedirects(response, reverse('dashboard'), fetch_redirect_response=False)

    # Teste para verificar se as páginas protegidas são renderizadas corretamente para usuários autenticados.
    def test_protected_pages_render_through_django(self):
        self.client.force_login(self.user)

        pages = {
            'dashboard': 'dashboard.js',
            'produtos': 'produtos.js',
            'novo_produto': 'novo_produto.js',
            'novo_cliente': 'novo_cliente.js',
            'estoque': 'estoque.js',
            'nova_venda': 'nova_venda.js',
            'clientes': 'clientes.js',
            'debitos': 'debitos.js',
            'mais_opcoes': 'mais_opcoes.js',
            'relatorios': 'relatorios.js',
            'compras': 'compras.js',
        }

        for route_name, script_name in pages.items():
            with self.subTest(route=route_name):
                response = self.client.get(reverse(route_name))

                self.assertEqual(response.status_code, 200)
                asset_path = f'estrela_modas/{script_name}'
                self.assertContains(response, f'src="/static/{asset_path}"')
                self.assertIsNotNone(finders.find(asset_path))
