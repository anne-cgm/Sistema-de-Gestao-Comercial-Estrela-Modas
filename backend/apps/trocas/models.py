from django.core.validators import MinValueValidator
from django.db import models

from apps.produtos.models import Produto
from apps.vendas.models import Venda


class Troca(models.Model):
    venda = models.ForeignKey('vendas.Venda', related_name='trocas', null=True, blank=True, on_delete=models.SET_NULL)
    produto_devolvido = models.ForeignKey('produtos.Produto', related_name='trocas_devolvidas', on_delete=models.PROTECT)
    produto_entregue = models.ForeignKey('produtos.Produto', related_name='trocas_entregues', null=True, blank=True, on_delete=models.PROTECT)
    motivo_troca = models.TextField()
    cupom_credito = models.DecimalField(max_digits=10, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    data_troca = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'estrela_modas_troca'
        ordering = ['-data_troca']
