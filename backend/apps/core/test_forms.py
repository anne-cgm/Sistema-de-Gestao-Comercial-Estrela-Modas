from decimal import Decimal
from django.test import TestCase
from apps.clientes.forms import ClienteForm
from apps.clientes.models import Cliente
from apps.clientes.forms import PagamentoDebitoForm
from apps.clientes.models import PagamentoDebito
from apps.produtos.forms import ProdutoForm
from apps.trocas.forms import TrocaForm
from apps.vendas.forms import ItemVendaForm
from apps.vendas.models import Venda

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

    def test_campos_monetarios_de_produto_continuam_numericos(self):
        form = ProdutoForm()

        self.assertEqual(form.fields['preco_custo'].widget.input_type, 'number')
        self.assertEqual(form.fields['preco_venda'].widget.input_type, 'number')

    def test_campos_de_novo_cliente_exibem_exemplos_de_formato(self):
        form = ClienteForm()

        self.assertEqual(form.fields['nome_cliente'].widget.attrs['placeholder'], 'Nome e sobrenome')
        self.assertEqual(form.fields['telefone'].widget.attrs['placeholder'], '(00) 00000 - 0000')

    def test_seletores_sem_escolha_usam_instrucoes_em_portugues(self):
        self.assertEqual(ItemVendaForm().fields['produto'].empty_label, 'Selecione um produto')
        self.assertEqual(PagamentoDebitoForm().fields['venda'].empty_label, 'Selecione uma dívida')

        form_troca = TrocaForm()
        self.assertEqual(form_troca.fields['venda'].empty_label, 'Selecione uma venda (opcional)')
        self.assertEqual(form_troca.fields['produto_devolvido'].empty_label, 'Selecione o produto devolvido')
        self.assertEqual(form_troca.fields['produto_entregue'].empty_label, 'Selecione o produto entregue')

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

    def test_lista_de_dividas_omite_venda_fiada_quitada(self):
        form_com_debito_aberto = PagamentoDebitoForm()
        self.assertIn(
            self.venda_fiada,
            form_com_debito_aberto.fields['venda'].queryset,
        )
        self.assertNotIn(
            self.venda_pix,
            form_com_debito_aberto.fields['venda'].queryset,
        )

        PagamentoDebito.objects.create(
            venda=self.venda_fiada,
            valor=Decimal('100.00'),
        )

        form = PagamentoDebitoForm()

        self.assertNotIn(
            self.venda_fiada,
            form.fields['venda'].queryset,
        )
        self.assertNotIn(
            self.venda_pix,
            form.fields['venda'].queryset,
        )

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
