from datetime import datetime, timezone as datetime_timezone
from decimal import Decimal
from django.contrib.auth import get_user_model
from django.http import response
from django.test import TestCase
from django.urls import reverse
from apps.clientes.models import Cliente
from apps.clientes.models import PagamentoDebito
from apps.vendas.models import Venda

class DebitosViewTests(TestCase):

# Testa: a view de débitos, incluindo registro de pagamentos parciais, tentativas de pagamento maior que o saldo devedor, tentativas de pagamento em dívida quitada e tentativas de pagamento para vendas sem débito.
# Esses testes verificam se a view está funcionando corretamente, se os formulários estão sendo processados corretamente e se os redirecionamentos e mensagens de erro estão sendo exibidos conforme esperado.

    def setUp(self):
        # Prepara os dados necessários antes de cada teste, criando um usuário teste para autenticação.
        self.user = get_user_model().objects.create_user(
            login='teste',
            nome='Usuário de teste',
            email='teste@email.com',
            password='senha-teste-123'
        )

        self.client.force_login(self.user)

        self.cliente = Cliente.objects.create(
            nome_cliente='Cliente Teste',
            telefone='11999999999',
        )

        self.venda_fiada = Venda.objects.create(
            cliente=self.cliente,
            valor_total=Decimal('100.00'),
            forma_pagamento=Venda.FormaPagamento.FIADO
        )

        self.venda_pix = Venda.objects.create(
            cliente=self.cliente,
            valor_total=Decimal('100.00'),
            forma_pagamento=Venda.FormaPagamento.PIX
        )

        # Define a URL para a página de débitos, que será usada nos testes para acessar a view correspondente.
        self.url = reverse('debitos')

    def test_pagina_debitos_carrega_corretamente(self):
        response = self.client.get(self.url) # Simula um navegador acessando a URL da página de débitos, e guarda toda a resposta do Django na variável response.

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.context['total_pendente'],
            Decimal('100.00')
        )

        # Pega a lista de vendas com débito do contexto da resposta, e verifica se o tamanho da lista é 1, ou seja, se há apenas uma venda com débito (a venda fiada criada no setUp).
        self.assertEqual(
            len(response.context['vendas_com_debito']),
            1
        )

    def test_pagina_nova_venda_preseleciona_cliente_da_url(self):
        response = self.client.get(
            reverse('nova_venda'),
            {'cliente': self.cliente.pk},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.context['form']['cliente'].value(),
            str(self.cliente.pk),
        )

    def test_registra_pagamento_parcial(self):
        # Simula o usuário preenchendo e enviando o formulário de pagamento parcial para a venda fiada. O método post envia os dados do formulário para a URL da página de débitos.
        response = self.client.post(self.url, {
            'venda': self.venda_fiada.id,
            'valor': '40.00',
            'observacoes': 'Pagamento parcial de teste'
        })

        # Verifica se o redirecionamento ocorreu corretamente para a mesma página de débitos após o envio do formulário, e se um novo registro de pagamento foi criado no banco de dados.
        self.assertRedirects(response, self.url)
        self.assertEqual(PagamentoDebito.objects.count(), 1)
        
        # Verifica se o saldo devedor da venda fiada foi atualizado corretamente após o pagamento parcial, e se o valor do saldo devedor é igual a 60.00 (100.00 - 40.00).
        self.venda_fiada.refresh_from_db()
        self.assertEqual(
            self.venda_fiada.saldo_devedor,
            Decimal('60.00')
        )

    def test_historico_de_recebimentos_exibe_valores_da_divida(self):
        primeiro_pagamento = PagamentoDebito.objects.create(
            venda=self.venda_fiada,
            valor=Decimal('40.00'),
        )
        segundo_pagamento = PagamentoDebito.objects.create(
            venda=self.venda_fiada,
            valor=Decimal('10.00'),
        )
        PagamentoDebito.objects.filter(pk=primeiro_pagamento.pk).update(
            data_pagamento=datetime(2026, 1, 2, 12, tzinfo=datetime_timezone.utc),
        )
        PagamentoDebito.objects.filter(pk=segundo_pagamento.pk).update(
            data_pagamento=datetime(2026, 1, 1, 12, tzinfo=datetime_timezone.utc),
        )

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        pagamentos = response.context['pagamentos_recentes']
        self.assertEqual(len(pagamentos), 2)
        self.assertEqual(
            [pagamento.pk for pagamento in pagamentos],
            [segundo_pagamento.pk, primeiro_pagamento.pk],
        )
        pagamentos_por_id = {pagamento.pk: pagamento for pagamento in pagamentos}
        primeiro = pagamentos_por_id[primeiro_pagamento.pk]
        segundo = pagamentos_por_id[segundo_pagamento.pk]
        self.assertEqual(primeiro.venda.valor_total, Decimal('100.00'))
        self.assertEqual(primeiro.valor, Decimal('40.00'))
        self.assertEqual(primeiro.total_pago_venda, Decimal('40.00'))
        self.assertEqual(primeiro.saldo_restante, Decimal('60.00'))
        self.assertEqual(segundo.venda.valor_total, Decimal('100.00'))
        self.assertEqual(segundo.valor, Decimal('10.00'))
        self.assertEqual(segundo.total_pago_venda, Decimal('50.00'))
        self.assertEqual(segundo.saldo_restante, Decimal('50.00'))

        self.assertContains(response, 'Valor original da dívida: R$ 100,00')
        self.assertContains(response, 'Total pago até agora: R$ 40,00')
        self.assertContains(response, 'Saldo restante: R$ 60,00')
        self.assertContains(response, 'Total pago até agora: R$ 50,00')
        self.assertContains(response, 'Saldo restante: R$ 50,00')
        self.assertContains(response, 'Este recebimento: R$ 40,00')
        self.assertContains(response, 'Este recebimento: R$ 10,00')

    def test_nao_registra_pagamento_maior_que_saldo(self):
        # Simula o envio de um formulário de pagamento com valor maior que o saldo devedor da venda fiada. O método post envia os dados do formulário para a URL da página de débitos.
        response = self.client.post(self.url, {
            'venda': self.venda_fiada.id,
            'valor': '150.00',
            'observacoes': 'Tentativa de pagamento maior que o saldo'
        })

        # Verifica se a resposta do Django foi um status code 200 (indicando que a página foi carregada corretamente), e se nenhum novo registro de pagamento foi criado no banco de dados, ou seja, o pagamento não foi registrado.
        self.assertEqual(response.status_code, 200)
        self.assertEqual(PagamentoDebito.objects.count(), 0)

        # Verifica se o saldo devedor da venda fiada permanece inalterado após a tentativa de pagamento inválido, e se o valor do saldo devedor é igual a 100.00 (o valor original da venda fiada).
        self.venda_fiada.refresh_from_db()
        self.assertEqual(
            self.venda_fiada.saldo_devedor,
            Decimal('100.00')
        )

    def test_nao_registra_pagamento_em_divida_quitada(self):
    # Primeiro, quita a dívida com um pagamento integral.
        PagamentoDebito.objects.create(
            venda=self.venda_fiada,
            valor=Decimal('100.00')
        )

        # Tenta registrar outro pagamento para a mesma venda.
        response = self.client.post(self.url, {
            'venda': self.venda_fiada.id,
            'valor': '10.00',
            'observacoes': 'Tentativa de pagamento em dívida quitada'
        })

        # A página deve ser exibida novamente, sem registrar o pagamento.
        self.assertEqual(response.status_code, 200)
        self.assertEqual(PagamentoDebito.objects.count(), 1)

        # Confirma que a dívida continua quitada.
        self.venda_fiada.refresh_from_db()
        self.assertEqual(
            self.venda_fiada.saldo_devedor,
            Decimal('0.00')
        )

    def test_nao_registra_pagamento_para_venda_sem_debito(self):
        # Simula o envio de um formulário de pagamento para uma venda que não possui débito (venda_pix). O método post envia os dados do formulário para a URL da página de débitos.
        response = self.client.post(self.url, {
            'venda': self.venda_pix.id,
            'valor': '10.00',
            'observacoes': 'Tentativa de pagamento para venda sem débito'
        })

        # Verifica se a resposta do Django foi um status code 200 (indicando que a página foi carregada corretamente), e se nenhum novo registro de pagamento foi criado no banco de dados, ou seja, o pagamento não foi registrado.
        self.assertEqual(response.status_code, 200)
        self.assertEqual(PagamentoDebito.objects.count(), 0)

        # Verifica se o saldo devedor da venda_pix permanece inalterado após a tentativa de pagamento inválido, e se o valor do saldo devedor é igual a 0.00 (indicando que não há débito).
        self.venda_pix.refresh_from_db()
        self.assertEqual(
            self.venda_pix.saldo_devedor,
            Decimal('0.00')
        )





        
