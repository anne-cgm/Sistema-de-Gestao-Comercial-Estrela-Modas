from django.contrib import admin

from .models import Cliente, PagamentoDebito


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nome_cliente', 'telefone')
    search_fields = ('nome_cliente', 'telefone')


@admin.register(PagamentoDebito)
class PagamentoDebitoAdmin(admin.ModelAdmin):
    list_display = ('id', 'venda', 'cliente', 'valor', 'data_pagamento')
    list_filter = ('data_pagamento',)
    search_fields = ('venda__id', 'venda__cliente__nome_cliente')
    readonly_fields = ('data_pagamento',)

    @admin.display(description='Cliente')
    def cliente(self, obj):
        return obj.venda.cliente.nome_cliente if obj.venda.cliente else 'Cliente não informado'
