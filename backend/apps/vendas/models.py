from django.db import models

class Despesa(models.Model):
    descricao = models.CharField(max_length=255)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data = models.DateField()
    categoria = models.CharField(max_length=100, blank=True, null=True)
    usuario = models.ForeignKey('usuarios.Usuario', on_delete=models.CASCADE, related_name='despesas')

    class Meta:
        db_table = 'despesa'


class Compra(models.Model):
    data = models.DateField()
    valorTotal = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    usuario = models.ForeignKey('usuarios.Usuario', on_delete=models.CASCADE, related_name='compras')

    class Meta:
        db_table = 'compra'


class ItemCompra(models.Model):
    quantidade = models.IntegerField()
    valor_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    
    compra = models.ForeignKey(Compra, on_delete=models.CASCADE, related_name='itens')
    variacao_produto = models.ForeignKey('produtos.VariacaoProduto', on_delete=models.RESTRICT)

    class Meta:
        db_table = 'item_compra'


class Venda(models.Model):
    data_hora = models.DateTimeField()
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    desconto = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    valor_total = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    forma_pagamento = models.CharField(max_length=5, null=True, blank=True)
    
    usuario = models.ForeignKey('usuarios.Usuario', on_delete=models.CASCADE, related_name='vendas')
    cliente = models.ForeignKey('clientes.Cliente', on_delete=models.SET_NULL, null=True, blank=True, related_name='vendas')

    class Meta:
        db_table = 'venda'


class ItemVenda(models.Model):
    quantidade = models.IntegerField()
    preco_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    tipo = models.CharField(max_length=50)
    
    venda = models.ForeignKey(Venda, on_delete=models.CASCADE, related_name='itens')
    variacao_produto = models.ForeignKey('produtos.VariacaoProduto', on_delete=models.RESTRICT)

    class Meta:
        db_table = 'item_venda'


class Troca(models.Model):
    data = models.DateField()
    diferenca_preco = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    possui_etiqueta = models.BooleanField(default=True)
    esta_manchado_ou_lavado = models.BooleanField(default=False)
    
    venda = models.ForeignKey(Venda, on_delete=models.CASCADE, related_name='trocas')

    class Meta:
        db_table = 'troca'


class ItemTroca(models.Model):
    quantidade = models.IntegerField()
    troca = models.ForeignKey(Troca, on_delete=models.CASCADE, related_name='itens')
    variacao_produto = models.ForeignKey('produtos.VariacaoProduto', on_delete=models.RESTRICT)

    class Meta:
        db_table = 'item_troca'


class Debito(models.Model):
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50)
    saldo_pendente = models.DecimalField(max_digits=10, decimal_places=2)
    
    venda = models.ForeignKey(Venda, on_delete=models.CASCADE, related_name='debitos')
    cliente = models.ForeignKey('clientes.Cliente', on_delete=models.RESTRICT, related_name='debitos')

    class Meta:
        db_table = 'debito'


class Pagamento(models.Model):
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data_hora = models.DateTimeField(auto_now_add=True)
    
    debito = models.ForeignKey(Debito, on_delete=models.CASCADE, related_name='pagamentos')

    class Meta:
        db_table = 'pagamento'