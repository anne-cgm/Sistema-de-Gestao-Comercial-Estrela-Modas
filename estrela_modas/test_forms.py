from decimal import Decimal
from django.test import TestCase
from .forms import PagamentoDebitoForm
from .models import Cliente, Venda, PagamentoDebito

class PagamentoDebitoFormTests(TestCase):

# Testa: validação do formulário de pagamento de débito, incluindo casos de venda não fiada, pagamento em dívida quitada e pagamento maior que o saldo devedor.
# Enquanto os testes dos modelos verificam se os cálculos estão corretos;
# os testes dos formulários verificam se os dados inválidos são barrados antes de serem processados.

    def setUp(self):
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

    # Método auxiliar para criar um formulário de pagamento de débito com os dados fornecidos. Evitar repetir a montagem do formulário em todos os testes.
    def criar_formulario(self, venda, valor):
        return PagamentoDebitoForm(data={
            'venda': venda.id,
            'valor': str(valor), # str serve para converter o valor decimal em string, pois o formulário espera uma string para o campo de valor.
            'observacoes': 'Pagamento de teste'
        })
    
    def test_aceita_pagamento_valido(self):
        form = self.criar_formulario(
            self.venda_fiada,
            Decimal('40.00')
        )

        # self.assertTrue(form.is_valid()) serve para verificar se o formulário é válido. Se o formulário não for válido, o teste falha.
        self.assertTrue(form.is_valid())

    def test_rejeita_venda_que_nao_e_fiada(self):
        form = self.criar_formulario(
            self.venda_pix,
            Decimal('40.00')
        )

        # Aqui estamos verificando duas coisas: que o formulário foi rejeitado e que o erro está especificamente associado ao campo valor.
        self.assertFalse(form.is_valid())
        self.assertIn('venda', form.errors)

    def test_rejeita_pagamento_em_divida_quitada(self):
        PagamentoDebito.objects.create(
            venda=self.venda_fiada,
            valor=Decimal('100.00')
        )

        form = self.criar_formulario(
            self.venda_fiada,
            Decimal('10.00')
        )

        self.assertFalse(form.is_valid())
        self.assertIn('venda', form.errors)

    def test_rejeita_pagamento_maior_que_saldo(self):
        # Simula um pagamento anterior de R$ 70.00 
        PagamentoDebito.objects.create(
            venda=self.venda_fiada,
            valor=Decimal('70.00')
        )

        # Tenta pagar mais R$ 40.00 (ultrapassando o saldo restante)
        form = self.criar_formulario(
            self.venda_fiada,
            Decimal('40.00')
        )

        self.assertFalse(form.is_valid())
        self.assertIn('valor', form.errors)
