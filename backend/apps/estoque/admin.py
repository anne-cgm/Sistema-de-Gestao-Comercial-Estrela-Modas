from django.contrib import admin

from .models import Compra, ItemCompra, MovimentacaoEstoque


class ItemCompraInline(admin.TabularInline):
    """Permite consultar os itens relacionados dentro da página da compra."""
    model = ItemCompra
    extra = 0


@admin.register(Compra)
class CompraAdmin(admin.ModelAdmin):
    """Apresenta os dados principais e os itens de cada compra no Admin."""
    list_display = ('id', 'fornecedor_nome', 'numero_nota_fiscal', 'data_chegada', 'valor_total')
    inlines = (ItemCompraInline,)


admin.site.register(MovimentacaoEstoque)
