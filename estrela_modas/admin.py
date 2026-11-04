from django.contrib import admin

from .models import (
    Cliente, Compra, Despesa, ItemCompra, ItemVenda, MovimentacaoEstoque,
    PagamentoDebito, Produto, Troca, Venda,
)


@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('nome_produto', 'sku', 'categoria', 'quantidade_estoque', 'preco_venda', 'ativo')
    list_filter = ('categoria', 'ativo')
    search_fields = ('nome_produto', 'sku', 'categoria')


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nome_cliente', 'cpf_cliente', 'telefone')
    search_fields = ('nome_cliente', 'cpf_cliente', 'telefone')


class ItemCompraInline(admin.TabularInline):
    model = ItemCompra
    extra = 0


@admin.register(Compra)
class CompraAdmin(admin.ModelAdmin):
    list_display = ('id', 'fornecedor_nome', 'numero_nota_fiscal', 'data_chegada', 'valor_total')
    inlines = (ItemCompraInline,)


class ItemVendaInline(admin.TabularInline):
    model = ItemVenda
    extra = 0


@admin.register(Venda)
class VendaAdmin(admin.ModelAdmin):
    list_display = ('id', 'data_venda', 'cliente', 'forma_pagamento', 'valor_total')
    list_filter = ('forma_pagamento', 'data_venda')
    inlines = (ItemVendaInline,)


admin.site.register((PagamentoDebito, Despesa, Troca, MovimentacaoEstoque))
