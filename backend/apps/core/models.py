"""Modelo usado pela tela de registro de despesas."""

from django.core.validators import MinValueValidator
from django.db import models


class Despesa(models.Model):
    descricao_despesa = models.CharField(max_length=180)
    categoria_despesa = models.CharField(max_length=80)
    valor_despesa = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01)],
    )
    data_despesa = models.DateField()
    observacoes = models.TextField(blank=True)

    class Meta:
        db_table = 'estrela_modas_despesa'
        ordering = ['-data_despesa']
        verbose_name = 'despesa'
        verbose_name_plural = 'despesas'

    def __str__(self):
        return self.descricao_despesa
