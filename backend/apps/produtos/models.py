from django.core.validators import MinValueValidator
from django.db import models


class Produto(models.Model):
    nome_produto = models.CharField(max_length=160)
    sku = models.CharField(max_length=64, unique=True)
    categoria = models.CharField(max_length=80, blank=True)
    tamanho = models.CharField(max_length=24, blank=True)
    cor = models.CharField(max_length=48, blank=True)
    preco_custo = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    preco_venda = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    quantidade_estoque = models.PositiveIntegerField(default=0)
    estoque_minimo = models.PositiveIntegerField(default=0)
    ativo = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'estrela_modas_produto'
        ordering = ['nome_produto', 'sku']
        verbose_name = 'produto'
        verbose_name_plural = 'produtos'

    def __str__(self):
        return f'{self.nome_produto} ({self.sku})'

    @property
    def estoque_baixo(self):
        return self.quantidade_estoque <= self.estoque_minimo
