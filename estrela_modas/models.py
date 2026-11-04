from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import Sum
from decimal import Decimal


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
        ordering = ['nome_produto', 'sku']
        verbose_name = 'produto'
        verbose_name_plural = 'produtos'

    def __str__(self):
        return f'{self.nome_produto} ({self.sku})'

    @property
    def estoque_baixo(self):
        return self.quantidade_estoque <= self.estoque_minimo


class Cliente(models.Model):
    nome_cliente = models.CharField(max_length=160)
    cpf_cliente = models.CharField(max_length=11, blank=True, unique=True, null=True)
    telefone = models.CharField(max_length=24, blank=True)
    endereco_completo = models.TextField(blank=True)
    limite_credito = models.DecimalField(max_digits=10, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['nome_cliente']
        verbose_name = 'cliente'
        verbose_name_plural = 'clientes'

    def __str__(self):
        return self.nome_cliente

    @property
    def saldo_devedor(self):
        total_fiado = self.vendas.filter(forma_pagamento=Venda.FormaPagamento.FIADO).aggregate(total=Sum('valor_total'))['total']
        total_pago = self.pagamentos_debito.aggregate(total=Sum('valor'))['total']
        return (total_fiado or Decimal('0.00')) - (total_pago or Decimal('0.00'))


class Compra(models.Model):
    fornecedor_nome = models.CharField(max_length=160, blank=True)
    numero_nota_fiscal = models.CharField(max_length=64, blank=True)
    data_chegada = models.DateTimeField(auto_now_add=True)
    valor_total = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    observacoes = models.TextField(blank=True)

    class Meta:
        ordering = ['-data_chegada']
        verbose_name = 'compra'
        verbose_name_plural = 'compras'

    def __str__(self):
        return f'Compra {self.pk} — {self.data_chegada:%d/%m/%Y}'


class ItemCompra(models.Model):
    compra = models.ForeignKey(Compra, related_name='itens', on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, related_name='itens_compra', on_delete=models.PROTECT)
    quantidade = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    preco_custo_unitario = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])

    @property
    def subtotal(self):
        return self.quantidade * self.preco_custo_unitario


class MovimentacaoEstoque(models.Model):
    class Tipo(models.TextChoices):
        ENTRADA = 'entrada', 'Entrada'
        SAIDA = 'saida', 'Saída'

    produto = models.ForeignKey(Produto, related_name='movimentacoes', on_delete=models.PROTECT)
    tipo = models.CharField(max_length=8, choices=Tipo.choices)
    quantidade = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    motivo = models.CharField(max_length=180)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-criado_em']
        verbose_name = 'movimentação de estoque'
        verbose_name_plural = 'movimentações de estoque'


class Venda(models.Model):
    class FormaPagamento(models.TextChoices):
        DINHEIRO = 'dinheiro', 'Dinheiro'
        PIX = 'pix', 'Pix'
        CARTAO = 'cartao', 'Cartão'
        FIADO = 'fiado', 'Fiado'

    cliente = models.ForeignKey(Cliente, related_name='vendas', null=True, blank=True, on_delete=models.SET_NULL)
    data_venda = models.DateTimeField(auto_now_add=True)
    desconto_aplicado = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    valor_total = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    forma_pagamento = models.CharField(max_length=12, choices=FormaPagamento.choices, default=FormaPagamento.PIX)

    class Meta:
        ordering = ['-data_venda']


class ItemVenda(models.Model):
    venda = models.ForeignKey(Venda, related_name='itens', on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, related_name='itens_venda', on_delete=models.PROTECT)
    quantidade = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    preco_unitario = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])

    @property
    def subtotal(self):
        return self.quantidade * self.preco_unitario


class PagamentoDebito(models.Model):
    cliente = models.ForeignKey(Cliente, related_name='pagamentos_debito', on_delete=models.PROTECT)
    valor = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)])
    data_pagamento = models.DateTimeField(auto_now_add=True)
    observacoes = models.CharField(max_length=240, blank=True)

    class Meta:
        ordering = ['-data_pagamento']
        verbose_name = 'pagamento de débito'
        verbose_name_plural = 'pagamentos de débito'


class Despesa(models.Model):
    descricao_despesa = models.CharField(max_length=180)
    categoria_despesa = models.CharField(max_length=80)
    valor_despesa = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)])
    data_despesa = models.DateField()
    observacoes = models.TextField(blank=True)

    class Meta:
        ordering = ['-data_despesa']
        verbose_name = 'despesa'
        verbose_name_plural = 'despesas'


class Troca(models.Model):
    venda = models.ForeignKey(Venda, related_name='trocas', null=True, blank=True, on_delete=models.SET_NULL)
    produto_devolvido = models.ForeignKey(Produto, related_name='trocas_devolvidas', on_delete=models.PROTECT)
    produto_entregue = models.ForeignKey(Produto, related_name='trocas_entregues', null=True, blank=True, on_delete=models.PROTECT)
    motivo_troca = models.TextField()
    cupom_credito = models.DecimalField(max_digits=10, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    data_troca = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-data_troca']
