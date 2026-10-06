from django.db import models

class Estoque(models.Model):
    quantidade = models.IntegerField(default=0)
    minimo = models.IntegerField(default=0)
    
    variacao_produto = models.OneToOneField(
        'produtos.VariacaoProduto', 
        on_delete=models.CASCADE, 
        related_name='estoque'
    )

    class Meta:
        db_table = 'estoque'

    def __str__(self):
        return f"Estoque: {self.quantidade} (Mín: {self.minimo})"


class MovimentacaoEstoque(models.Model):
    tipo = models.CharField(max_length=50)
    quantidade = models.IntegerField()
    data_hora = models.DateTimeField(auto_now_add=True)
    
    estoque = models.ForeignKey(Estoque, on_delete=models.CASCADE, related_name='movimentacoes')

    class Meta:
        db_table = 'movimentacao_estoque'

    def __str__(self):
        return f"{self.tipo} - Qtd: {self.quantidade}"