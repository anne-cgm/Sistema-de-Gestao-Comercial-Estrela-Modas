from django.contrib import admin

from .models import Compra, ItemCompra, MovimentacaoEstoque


class ItemCompraInline(admin.TabularInline):
    model = ItemCompra
    extra = 0


@admin.register(Compra)
class CompraAdmin(admin.ModelAdmin):
    list_display = ('id', 'fornecedor_nome', 'numero_nota_fiscal', 'data_chegada', 'valor_total')
    inlines = (ItemCompraInline,)


admin.site.register(MovimentacaoEstoque)
