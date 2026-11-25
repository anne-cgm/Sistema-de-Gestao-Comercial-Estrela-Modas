from django.contrib import admin

from .models import ItemVenda, Venda


class ItemVendaInline(admin.TabularInline):
    model = ItemVenda
    extra = 0


@admin.register(Venda)
class VendaAdmin(admin.ModelAdmin):
    list_display = ('id', 'data_venda', 'cliente', 'forma_pagamento', 'valor_total')
    list_filter = ('forma_pagamento', 'data_venda')
    inlines = (ItemVendaInline,)
