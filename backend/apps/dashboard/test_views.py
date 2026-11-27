"""Testes das consultas e dos indicadores exibidos no dashboard."""

from datetime import datetime, time, timedelta
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from apps.clientes.models import Cliente, PagamentoDebito
from apps.core.models import Despesa
from apps.produtos.models import Produto
from apps.usuarios.models import ConfiguracaoPermissoesFuncionarios
from apps.vendas.models import ItemVenda, Venda


class DashboardViewTests(TestCase):
    """Exercita os períodos e os dados que a view agrega do banco."""

    def setUp(self):
        # Cada teste usa uma conta autenticada sem privilégios administrativos.
        self.usuario = get_user_model().objects.create_user(
            login='dashboard-teste',
            nome='Usuário do dashboard',
            email='dashboard@example.com',
            password='senha-de-teste',
        )
        ConfiguracaoPermissoesFuncionarios.objects.create(
            permissoes=['dashboard'],
        )
        self.client.force_login(self.usuario)
        self.url = reverse('dashboard')
        self.hoje = timezone.localdate()
        self.produto = Produto.objects.create(
            nome_produto='Blusa de teste',
            sku='DASH-001',
            preco_custo=Decimal('5.00'),
            preco_venda=Decimal('10.00'),
            quantidade_estoque=2,
            estoque_minimo=3,
            qr_code='dashboard-teste.png',
        )

    def criar_venda(self, dia, hora, valor, forma_pagamento, cliente=None):
        """Cria uma venda e ajusta o horário para testar filtros por data/hora."""
        venda = Venda.objects.create(
            cliente=cliente,
            valor_total=Decimal(valor),
            forma_pagamento=forma_pagamento,
        )
        instante = timezone.make_aware(datetime.combine(dia, time(hora)))
        Venda.objects.filter(pk=venda.pk).update(data_venda=instante)
        venda.refresh_from_db()
        return venda

    def adicionar_item(self, venda, quantidade=1):
        """Registra o item vendido para os cálculos de lucro e ranking."""
        return ItemVenda.objects.create(
            venda=venda,
            produto=self.produto,
            quantidade=quantidade,
            preco_unitario=Decimal('10.00'),
        )

    def test_pagina_exige_autenticacao(self):
        """Usuários sem sessão são encaminhados para o login."""
        self.client.logout()

        resposta = self.client.get(self.url)

        self.assertEqual(resposta.status_code, 302)
        self.assertIn('/login/', resposta.url)

    def test_filtro_hoje_calcula_indicadores_horarios_e_despesas(self):
        """O filtro de hoje inclui só vendas/despesas de hoje e mostra 09–19h."""
        venda_manha = self.criar_venda(
            self.hoje,
            9,
            '20.00',
            Venda.FormaPagamento.PIX,
        )
        venda_fim_dia = self.criar_venda(
            self.hoje,
            18,
            '30.00',
            Venda.FormaPagamento.CARTAO,
        )
        venda_anterior = self.criar_venda(
            self.hoje - timedelta(days=1),
            12,
            '100.00',
            Venda.FormaPagamento.DINHEIRO,
        )
        self.adicionar_item(venda_manha)
        self.adicionar_item(venda_fim_dia, quantidade=2)
        self.adicionar_item(venda_anterior, quantidade=10)
        Despesa.objects.create(
            descricao_despesa='Embalagens',
            categoria_despesa='Materiais',
            valor_despesa=Decimal('8.00'),
            data_despesa=self.hoje,
        )
        Despesa.objects.create(
            descricao_despesa='Despesa anterior',
            categoria_despesa='Materiais',
            valor_despesa=Decimal('50.00'),
            data_despesa=self.hoje - timedelta(days=1),
        )

        resposta = self.client.get(self.url, {'periodo': 'hoje'})

        self.assertEqual(resposta.status_code, 200)
        self.assertEqual(resposta.context['total_vendas_periodo'], Decimal('50.00'))
        self.assertEqual(resposta.context['quantidade_vendas_periodo'], 2)
        self.assertEqual(resposta.context['ticket_medio'], Decimal('25.00'))
        self.assertEqual(resposta.context['lucro_estimado'], Decimal('35.00'))
        self.assertEqual(resposta.context['total_despesas_periodo'], Decimal('8.00'))
        self.assertEqual(resposta.context['quantidade_despesas_periodo'], 1)
        self.assertEqual(len(resposta.context['vendas_por_intervalo']), 10)
        self.assertEqual(resposta.context['vendas_por_intervalo'][0]['rotulo'], '09–10h')
        self.assertEqual(resposta.context['vendas_por_intervalo'][-1]['rotulo'], '18–19h')
        self.assertEqual(resposta.context['vendas_por_intervalo'][0]['total'], Decimal('20.00'))
        self.assertEqual(resposta.context['vendas_por_intervalo'][-1]['total'], Decimal('30.00'))
        self.assertEqual(
            list(resposta.context['mais_vendidos'])[0]['unidades'],
            3,
        )

    def test_filtro_sete_dias_inclui_inicio_e_exclui_dia_anterior(self):
        """O intervalo semanal contém hoje e os seis dias anteriores."""
        venda_inicio = self.criar_venda(
            self.hoje - timedelta(days=6),
            10,
            '25.00',
            Venda.FormaPagamento.PIX,
        )
        self.criar_venda(
            self.hoje - timedelta(days=7),
            10,
            '99.00',
            Venda.FormaPagamento.PIX,
        )
        self.adicionar_item(venda_inicio)

        resposta = self.client.get(self.url, {'periodo': 'semana'})

        self.assertEqual(resposta.status_code, 200)
        self.assertEqual(resposta.context['total_vendas_periodo'], Decimal('25.00'))
        self.assertEqual(len(resposta.context['vendas_por_intervalo']), 7)

    def test_filtro_mes_agrupa_vendas_e_produtos_no_mes_atual(self):
        """O mês atual considera só as vendas e os itens do mês selecionado."""
        venda_mes = self.criar_venda(
            self.hoje.replace(day=1),
            11,
            '40.00',
            Venda.FormaPagamento.DINHEIRO,
        )
        venda_mes_anterior = self.criar_venda(
            self.hoje.replace(day=1) - timedelta(days=1),
            11,
            '200.00',
            Venda.FormaPagamento.PIX,
        )
        self.adicionar_item(venda_mes, quantidade=4)
        self.adicionar_item(venda_mes_anterior, quantidade=20)

        resposta = self.client.get(self.url, {'periodo': 'mes'})

        self.assertEqual(resposta.status_code, 200)
        self.assertEqual(resposta.context['total_vendas_periodo'], Decimal('40.00'))
        self.assertEqual(resposta.context['quantidade_vendas_periodo'], 1)
        self.assertEqual(resposta.context['mais_vendidos'][0]['unidades'], 4)
        self.assertTrue(resposta.context['vendas_por_intervalo'])

    def test_resumo_de_pagamento_e_debitos_fiados_vem_do_banco(self):
        """Agrupa pagamentos por forma e calcula saldos fiados em aberto."""
        cliente_a = Cliente.objects.create(nome_cliente='Cliente A')
        cliente_b = Cliente.objects.create(nome_cliente='Cliente B')
        self.criar_venda(
            self.hoje,
            12,
            '60.00',
            Venda.FormaPagamento.PIX,
        )
        venda_fiada_a = self.criar_venda(
            self.hoje - timedelta(days=20),
            12,
            '100.00',
            Venda.FormaPagamento.FIADO,
            cliente_a,
        )
        self.criar_venda(
            self.hoje - timedelta(days=15),
            12,
            '50.00',
            Venda.FormaPagamento.FIADO,
            cliente_b,
        )
        PagamentoDebito.objects.create(
            venda=venda_fiada_a,
            valor=Decimal('30.00'),
            observacoes='Pagamento parcial',
        )

        resposta = self.client.get(self.url, {'periodo': 'hoje'})

        pagamentos = resposta.context['pagamentos_periodo']
        self.assertEqual(len(pagamentos), 1)
        self.assertEqual(pagamentos[0]['metodo'], 'Pix')
        self.assertEqual(pagamentos[0]['total'], Decimal('60.00'))
        self.assertEqual(pagamentos[0]['percentual'], 100)
        self.assertEqual(resposta.context['saldo_fiado_pendente'], Decimal('120.00'))
        self.assertEqual(resposta.context['clientes_com_debito'], 2)

    def test_estoque_critico_reflete_quantidade_atual_do_produto(self):
        """O painel inclui produto cuja quantidade está no limite mínimo."""
        resposta = self.client.get(self.url)

        self.assertEqual(resposta.context['quantidade_produtos'], 1)
        self.assertEqual(resposta.context['quantidade_estoque_baixo'], 1)
        self.assertEqual(resposta.context['produtos_baixo'][0], self.produto)
