from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import Sum

from apps.clientes.models import Cliente
from apps.produtos.models import Produto


class Venda(models.Model):
    class FormaPagamento(models.TextChoices):
        DINHEIRO = 'dinheiro', 'Dinheiro'
        PIX = 'pix', 'Pix'
        CARTAO = 'cartao', 'Cartão'
        FIADO = 'fiado', 'Fiado'

    cliente = models.ForeignKey('clientes.Cliente', related_name='vendas', null=True, blank=True, on_delete=models.SET_NULL)
    data_venda = models.DateTimeField(auto_now_add=True)
    desconto_aplicado = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    valor_total = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    forma_pagamento = models.CharField(max_length=12, choices=FormaPagamento.choices, default=FormaPagamento.PIX)

    class Meta:
        db_table = 'estrela_modas_venda'
        ordering = ['-data_venda']

# Essas propriedades calculam o total pago, o saldo devedor e a situação do débito para vendas com forma de pagamento "fiado".
    @property
    def total_pago(self):
        return self.pagamentos.aggregate(
            total_pago=Sum('valor')
        )['total_pago'] or Decimal('0.00')

    @property
    def saldo_devedor(self):
        if self.forma_pagamento != self.FormaPagamento.FIADO:
            return Decimal('0.00')
        return self.valor_total - self.total_pago

    @property 
    def situacao_debito(self):
        if self.forma_pagamento != self.FormaPagamento.FIADO:
            return 'nao_se_aplica'
        if self.saldo_devedor <= 0:
            return 'quitada'
        if self.total_pago > 0:
            return 'parcial'
        return 'aberta'


class ItemVenda(models.Model):
    venda = models.ForeignKey(Venda, related_name='itens', on_delete=models.CASCADE)
    produto = models.ForeignKey('produtos.Produto', related_name='itens_venda', on_delete=models.PROTECT)
    quantidade = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    preco_unitario = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])

    @property
    def subtotal(self):
        return self.quantidade * self.preco_unitario

    class Meta:
        db_table = 'estrela_modas_itemvenda'
