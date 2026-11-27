"""Testes do registro de compras e dos efeitos no estoque."""

from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from apps.estoque.models import Compra, ItemCompra, MovimentacaoEstoque
from apps.produtos.models import Produto


class ComprasViewTests(TestCase):
    """Confere acesso, validação e gravação do fluxo de compras."""

    def setUp(self):
        # Mantém os testes isolados usando um funcionário autenticado.
        self.usuario = get_user_model().objects.create_user(
            login='teste-compras',
            nome='Funcionária de teste',
            email='compras@example.com',
            password='senha-de-teste',
        )
        self.client.force_login(self.usuario)
        self.url = reverse('compras')

        # O nome preenchido evita gerar um QR Code durante a criação do registro.
        self.produto = Produto.objects.create(
            nome_produto='Blusa de teste',
            sku='COMPRA-001',
            preco_custo=Decimal('12.00'),
            preco_venda=Decimal('25.00'),
            quantidade_estoque=4,
            estoque_minimo=2,
            qr_code='qrcodes/compra-teste.png',
        )

    def dados_compra(self, **alteracoes):
        """Monta um POST válido e permite sobrescrever um campo em cada cenário."""
        dados = {
            'produto': str(self.produto.pk),
            'quantidade': '3',
            'preco_custo_unitario': '15.50',
            # Fornecedor e nota são intencionalmente opcionais.
        }
        dados.update(alteracoes)
        return dados

    def test_pagina_de_compras_exige_login(self):
        """Usuários sem sessão são encaminhados para a página de login."""
        self.client.logout()

        resposta = self.client.get(self.url)

        self.assertEqual(resposta.status_code, 302)
        self.assertIn('/login/', resposta.url)

    def test_get_exibe_formulario_e_compras_recentes(self):
        """A tela carrega os produtos ativos e a lista de compras já registradas."""
        resposta = self.client.get(self.url)

        self.assertEqual(resposta.status_code, 200)
        self.assertContains(resposta, 'Registrar compra')
        self.assertIn(self.produto, resposta.context['form'].fields['produto'].queryset)
        self.assertEqual(resposta.context['compras_recentes'].count(), 0)

    def test_registro_sem_fornecedor_atualiza_compra_item_e_estoque(self):
        """Uma compra sem fornecedor ou nota grava todos os efeitos de estoque."""
        resposta = self.client.post(self.url, self.dados_compra(), follow=True)

        self.assertEqual(resposta.status_code, 200)
        self.assertContains(resposta, 'Compra registrada e estoque atualizado.')

        compra = Compra.objects.get()
        item = ItemCompra.objects.get(compra=compra)
        self.produto.refresh_from_db()

        # O valor total vem do custo unitário multiplicado pela quantidade recebida.
        self.assertEqual(compra.fornecedor_nome, '')
        self.assertEqual(compra.numero_nota_fiscal, '')
        self.assertEqual(compra.valor_total, Decimal('46.50'))
        self.assertEqual(item.produto, self.produto)
        self.assertEqual(item.quantidade, 3)
        self.assertEqual(item.preco_custo_unitario, Decimal('15.50'))

        # A entrada aumenta o estoque e registra o custo da compra mais recente.
        self.assertEqual(self.produto.quantidade_estoque, 7)
        self.assertEqual(self.produto.preco_custo, Decimal('15.50'))
        movimentacao = MovimentacaoEstoque.objects.get()
        self.assertEqual(movimentacao.produto, self.produto)
        self.assertEqual(movimentacao.tipo, MovimentacaoEstoque.Tipo.ENTRADA)
        self.assertEqual(movimentacao.quantidade, 3)
        self.assertEqual(movimentacao.motivo, f'Entrada da compra #{compra.pk}')

    def test_registro_com_fornecedor_e_nota_persiste_dados_opcionais(self):
        """Fornecedor e nota são salvos quando a loja informa esses dados."""
        self.client.post(self.url, self.dados_compra(
            fornecedor_nome='  Fornecedor do bairro  ',
            numero_nota_fiscal='  NF-123  ',
        ))

        compra = Compra.objects.get()
        self.assertEqual(compra.fornecedor_nome, 'Fornecedor do bairro')
        self.assertEqual(compra.numero_nota_fiscal, 'NF-123')

    def test_quantidade_invalida_nao_registra_compra_nem_altera_estoque(self):
        """Uma quantidade zero é rejeitada sem criar registros parciais."""
        resposta = self.client.post(self.url, self.dados_compra(quantidade='0'))

        self.assertEqual(resposta.status_code, 200)
        self.assertTrue(resposta.context['form'].errors)
        self.assertEqual(Compra.objects.count(), 0)
        self.assertEqual(ItemCompra.objects.count(), 0)
        self.assertEqual(MovimentacaoEstoque.objects.count(), 0)
        self.produto.refresh_from_db()
        self.assertEqual(self.produto.quantidade_estoque, 4)
        self.assertEqual(self.produto.preco_custo, Decimal('12.00'))

    def test_produto_inativo_nao_pode_ser_comprado(self):
        """Produtos desativados não aparecem como opção válida no formulário."""
        self.produto.ativo = False
        self.produto.save(update_fields=['ativo'])

        resposta = self.client.post(self.url, self.dados_compra())

        self.assertEqual(resposta.status_code, 200)
        self.assertIn('produto', resposta.context['form'].errors)
        self.assertEqual(Compra.objects.count(), 0)
        self.assertEqual(MovimentacaoEstoque.objects.count(), 0)

    def test_formulario_vazio_mantem_erros_de_validacao(self):
        """Um POST vazio continua vinculado e apresenta os campos obrigatórios."""
        resposta = self.client.post(self.url, {})

        self.assertEqual(resposta.status_code, 200)
        self.assertTrue(resposta.context['form'].is_bound)
        self.assertIn('produto', resposta.context['form'].errors)
        self.assertIn('quantidade', resposta.context['form'].errors)
        self.assertEqual(Compra.objects.count(), 0)
