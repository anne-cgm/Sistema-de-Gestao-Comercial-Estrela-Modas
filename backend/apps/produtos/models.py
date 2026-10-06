from django.db import models

class Categoria(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'categoria'

    def __str__(self):
        return self.nome


class Produto(models.Model):
    sku_pai = models.CharField(max_length=50, unique=True)
    nome = models.CharField(max_length=255)
    descricao = models.TextField(blank=True, null=True)
    material = models.CharField(max_length=100, blank=True, null=True)
    estampa = models.CharField(max_length=100, blank=True, null=True)
    composicao = models.CharField(max_length=100, blank=True, null=True)
    preco_custo = models.DecimalField(max_digits=10, decimal_places=2)
    preco_venda = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.BooleanField(default=True)
    
    categoria = models.ForeignKey(Categoria, on_delete=models.RESTRICT, related_name='produtos')

    class Meta:
        db_table = 'produto'

    def __str__(self):
        return f"{self.sku_pai} - {self.nome}"


class VariacaoProduto(models.Model):
    sku = models.CharField(max_length=50, unique=True)
    tamanho = models.CharField(max_length=20)
    cor = models.CharField(max_length=50)
    codigo_qr = models.CharField(max_length=255, blank=True, null=True)
    
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE, related_name='variacoes')

    class Meta:
        db_table = 'variacao_produto'

    def __str__(self):
        return f"{self.sku} ({self.tamanho}/{self.cor})"