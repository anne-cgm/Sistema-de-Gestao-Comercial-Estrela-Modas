from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models

from django.apps import apps as django_apps


class Cliente(models.Model):
    nome_cliente = models.CharField(max_length=160)
    telefone = models.CharField(max_length=24, blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'estrela_modas_cliente'
        ordering = ['nome_cliente']
        verbose_name = 'cliente'
        verbose_name_plural = 'clientes'

    def __str__(self):
        return self.nome_cliente

# Calcula o saldo devedor do cliente considerando apenas as vendas fiadas (forma de pagamento "fiado").
    @property
    def saldo_devedor(self):
        Venda = django_apps.get_model('vendas', 'Venda')
        vendas_fiadas = self.vendas.filter(
            forma_pagamento=Venda.FormaPagamento.FIADO
        )

        return sum(
            (venda.saldo_devedor for venda in vendas_fiadas),
            Decimal('0.00')
        )

# Associa pagamentos diretamente à venda, permitindo o cálculo correto do saldo devedor e da situação do débito.
class PagamentoDebito(models.Model):
    venda = models.ForeignKey(
        'vendas.Venda',
        related_name='pagamentos',
        on_delete=models.PROTECT,
    )
    valor = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01)],
    )
    data_pagamento = models.DateTimeField(auto_now_add=True)
    observacoes = models.CharField(max_length=240, blank=True)

    class Meta:
        db_table = 'estrela_modas_pagamentodebito'
        verbose_name = 'Pagamento de débito'
        verbose_name_plural = 'Pagamentos de débitos'

    def __str__(self):
        return f'Pagamento da venda #{self.venda_id} - R$ {self.valor}'
