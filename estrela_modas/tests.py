from django.contrib.staticfiles import finders
from django.test import SimpleTestCase
from django.urls import reverse


class PageRoutingTests(SimpleTestCase):
    def test_home_redirects_to_login(self):
        response = self.client.get('/')

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, reverse('login'))

    def test_frontend_pages_render_through_django(self):
        pages = {
            'login': 'login.js',
            'dashboard': 'dashboard.js',
            'produtos': 'produtos.js',
            'cadastro_produto': 'cadastro_produto.js',
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
