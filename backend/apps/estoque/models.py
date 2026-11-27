from django.core.validators import MinValueValidator
from django.db import models

from apps.produtos.models import Produto


class Compra(models.Model):
    """Cabeçalho da compra que agrupa seus itens e dados opcionais do fornecedor."""

    # Fornecedor e nota podem ficar vazios em compras feitas sem um fornecedor formal.
    fornecedor_nome = models.CharField(max_length=160, blank=True)
    numero_nota_fiscal = models.CharField(max_length=64, blank=True)
    data_chegada = models.DateTimeField(auto_now_add=True)
    valor_total = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    observacoes = models.TextField(blank=True)

    class Meta:
        db_table = 'estrela_modas_compra'
        ordering = ['-data_chegada']
        verbose_name = 'compra'
        verbose_name_plural = 'compras'

    def __str__(self):
        return f'Compra {self.pk} — {self.data_chegada:%d/%m/%Y}'


class ItemCompra(models.Model):
    """Produto, quantidade e custo unitário que compõem uma compra."""

    # O produto não pode ser removido enquanto existir registro de compra ligado a ele.
    compra = models.ForeignKey(Compra, related_name='itens', on_delete=models.CASCADE)
    produto = models.ForeignKey('produtos.Produto', related_name='itens_compra', on_delete=models.PROTECT)
    quantidade = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    preco_custo_unitario = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])

    @property
    def subtotal(self):
        """Calcula o custo total deste item sem persistir um valor duplicado."""
        return self.quantidade * self.preco_custo_unitario

    class Meta:
        db_table = 'estrela_modas_itemcompra'


class MovimentacaoEstoque(models.Model):
    """Histórico de entradas e saídas de unidades de cada produto."""

    class Tipo(models.TextChoices):
        # Os rótulos são exibidos no Django Admin; os valores são gravados no banco.
        ENTRADA = 'entrada', 'Entrada'
        SAIDA = 'saida', 'Saída'

    produto = models.ForeignKey('produtos.Produto', related_name='movimentacoes', on_delete=models.PROTECT)
    tipo = models.CharField(max_length=8, choices=Tipo.choices)
    quantidade = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    motivo = models.CharField(max_length=180)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'estrela_modas_movimentacaoestoque'
        ordering = ['-criado_em']
        verbose_name = 'movimentação de estoque'
        verbose_name_plural = 'movimentações de estoque'
