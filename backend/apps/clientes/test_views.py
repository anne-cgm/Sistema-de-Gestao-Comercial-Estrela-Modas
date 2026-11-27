from datetime import datetime, timezone as datetime_timezone
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .forms import PagamentoDebitoForm
from apps.vendas.models import Venda
from apps.usuarios.models import ConfiguracaoPermissoesFuncionarios
from .models import Cliente, PagamentoDebito


class ClienteDetalhesViewTests(TestCase):
    def setUp(self):
        user = get_user_model().objects.create_user(
            login='teste',
            nome='Usuário de teste',
            email='teste@email.com',
            password='senha-teste-123',
        )
        ConfiguracaoPermissoesFuncionarios.objects.create(
            permissoes=['clientes'],
        )
        self.client.force_login(user)
        self.cliente = Cliente.objects.create(
            nome_cliente='Cliente Teste',
            telefone='11999999999',
        )

    def test_pagina_de_detalhes_carrega_em_requisicao_get(self):
        response = self.client.get(
            reverse('cliente_detalhes', kwargs={'pk': self.cliente.pk})
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Cliente Teste')
        self.assertNotContains(response, 'Informe o nome completo do cliente.')
        self.assertContains(
            response,
            f'href="{reverse("nova_venda")}?cliente={self.cliente.pk}"',
        )

    def test_pagina_de_detalhes_exibe_dialogo_de_confirmacao(self):
        response = self.client.get(
            reverse('cliente_detalhes', kwargs={'pk': self.cliente.pk})
        )

        self.assertContains(response, 'data-dialogo-excluir')
        self.assertContains(response, 'Confirmar exclusão')
        self.assertContains(
            response,
            reverse('excluir_cliente', kwargs={'pk': self.cliente.pk}),
        )
        conteudo = response.content.decode()
        posicoes_botoes = [
            conteudo.index('Salvar alterações'),
            conteudo.index('Excluir cliente'),
            conteudo.index('Nova venda'),
            conteudo.index('Consultar débitos'),
        ]
        self.assertEqual(posicoes_botoes, sorted(posicoes_botoes))

    def test_excluir_cliente_preserva_venda_e_pagamento(self):
        venda = Venda.objects.create(
            cliente=self.cliente,
            valor_total=Decimal('10.00'),
            forma_pagamento=Venda.FormaPagamento.FIADO,
        )
        pagamento = PagamentoDebito.objects.create(
            venda=venda,
            valor=Decimal('10.00'),
        )

        response = self.client.post(
            reverse('excluir_cliente', kwargs={'pk': self.cliente.pk})
        )

        self.assertRedirects(response, reverse('clientes'))
        self.assertFalse(Cliente.objects.filter(pk=self.cliente.pk).exists())
        venda.refresh_from_db()
        self.assertIsNone(venda.cliente)
        self.assertTrue(PagamentoDebito.objects.filter(pk=pagamento.pk).exists())

    def test_nao_exclui_cliente_com_debito_pendente_e_exibe_aviso(self):
        Venda.objects.create(
            cliente=self.cliente,
            valor_total=Decimal('10.00'),
            forma_pagamento=Venda.FormaPagamento.FIADO,
        )

        response = self.client.post(
            reverse('excluir_cliente', kwargs={'pk': self.cliente.pk})
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(Cliente.objects.filter(pk=self.cliente.pk).exists())
        self.assertContains(
            response,
            'Não é possível excluir este cliente enquanto houver débitos pendentes.',
        )
        self.assertContains(response, 'data-erro-detalhes')

    def test_exclusao_de_cliente_nao_aceita_requisicao_get(self):
        response = self.client.get(
            reverse('excluir_cliente', kwargs={'pk': self.cliente.pk})
        )

        self.assertEqual(response.status_code, 405)
        self.assertTrue(Cliente.objects.filter(pk=self.cliente.pk).exists())

    def test_rotulo_de_venda_usa_horario_local_de_sao_paulo(self):
        venda = Venda.objects.create(
            cliente=self.cliente,
            valor_total=Decimal('10.00'),
            forma_pagamento=Venda.FormaPagamento.FIADO,
        )
        Venda.objects.filter(pk=venda.pk).update(
            data_venda=datetime(2025, 3, 14, 15, tzinfo=datetime_timezone.utc)
        )
        venda.refresh_from_db()

        with timezone.override('UTC'):
            rotulo = PagamentoDebitoForm().label_from_instance(venda)

        self.assertIn('14/03/2025 12:00', rotulo)
