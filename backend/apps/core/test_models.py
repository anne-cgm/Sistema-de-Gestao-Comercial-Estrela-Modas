from decimal import Decimal
from django.test import TestCase
from apps.clientes.models import Cliente
from apps.clientes.models import PagamentoDebito
from apps.vendas.models import Venda

class VendaDebitoTests(TestCase):

# Testa: venda comum, venda fiada, pagamentos parciais e integrais, e soma de dívidas do cliente.
# Esses testes verificam os cálculos e as propriedades dos modelos. Eles não garantem que o formulário ou a view impençam um pagamento inválido.
    
    def setUp(self):
        # Cria um cliente de teste
        self.cliente = Cliente.objects.create(
            nome_cliente='Cliente Teste',
            telefone='11999999999',
        )

    def criar_venda_fiada(self, valor='100.00'):
        # Método auxiliar para repetir a criação de uma venda fiada
        return Venda.objects.create(
            cliente=self.cliente,
            valor_total=Decimal(valor),
            forma_pagamento=Venda.FormaPagamento.FIADO
        )
    
    def test_venda_comum_nao_gera_debito(self):
        venda = Venda.objects.create(
            cliente=self.cliente,
            valor_total=Decimal('100.00'),
            forma_pagamento=Venda.FormaPagamento.PIX
        )

        # self.assertEqual serve para verificar se o valor esperado é igual ao valor retornado pelo código. Se não forem iguais, o teste falha.
        self.assertEqual(venda.saldo_devedor, Decimal('0.00'))
        self.assertEqual(venda.situacao_debito, 'nao_se_aplica')

    def test_venda_fiada_sem_pagamentos_tem_saldo_integral(self):
        venda = self.criar_venda_fiada()

        self.assertEqual(venda.total_pago, Decimal('0.00'))
        self.assertEqual(venda.saldo_devedor, Decimal('100.000'))
        self.assertEqual(venda.situacao_debito, 'aberta')

    def test_pagamento_parcial_reduz_saldo_devedor(self):
        venda = self.criar_venda_fiada()

        PagamentoDebito.objects.create(
            venda=venda,
            valor=Decimal('30.00')
        )

        venda.refresh_from_db() 

        self.assertEqual(venda.total_pago, Decimal('30.00'))
        self.assertEqual(venda.saldo_devedor, Decimal('70.00'))
        self.assertEqual(venda.situacao_debito, 'parcial')

    def test_pagamento_integral_quita_debito(self):
        venda = self.criar_venda_fiada()

        PagamentoDebito.objects.create(
            venda=venda,
            valor=Decimal('100.00')
        )

        venda.refresh_from_db()

        self.assertEqual(venda.total_pago, Decimal('100.00'))
        self.assertEqual(venda.saldo_devedor, Decimal('0.00'))
        self.assertEqual(venda.situacao_debito, 'quitada')

    def test_cliente_soma_dividas_de_todas_as_vendas_fiadas(self):
        venda1 = self.criar_venda_fiada(valor='100.00')
        venda2 = self.criar_venda_fiada(valor='200.00')

        PagamentoDebito.objects.create(
            venda=venda1,
            valor=Decimal('40.00')
        )

        PagamentoDebito.objects.create(
            venda=venda2,
            valor=Decimal('50.00')
        )

        self.cliente.refresh_from_db()

        self.assertEqual(
            self.cliente.saldo_devedor, 
            Decimal('210.00'))  
