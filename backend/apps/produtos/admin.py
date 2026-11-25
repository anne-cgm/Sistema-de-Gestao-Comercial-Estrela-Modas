from django.contrib import admin

from .models import Produto


@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('nome_produto', 'sku', 'categoria', 'quantidade_estoque', 'preco_venda', 'ativo')
    list_filter = ('categoria', 'ativo')
    search_fields = ('nome_produto', 'sku', 'categoria')
