from django import forms

from .models import Produto


class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = [
            'nome_produto', 'sku', 'categoria', 'tamanho', 'cor',
            'preco_custo', 'preco_venda', 'quantidade_estoque', 'estoque_minimo',
        ]
        labels = {
            'nome_produto': 'Nome do produto',
            'sku': 'SKU / código do QR',
            'categoria': 'Categoria',
            'tamanho': 'Tamanho',
            'cor': 'Cor',
            'preco_custo': 'Preço de custo',
            'preco_venda': 'Preço de venda',
            'quantidade_estoque': 'Quantidade inicial',
            'estoque_minimo': 'Estoque mínimo',
        }
        widgets = {
            'nome_produto': forms.TextInput(attrs={'class': 'input'}),
            'sku': forms.TextInput(attrs={'class': 'input'}),
            'categoria': forms.TextInput(attrs={'class': 'input'}),
            'tamanho': forms.TextInput(attrs={'class': 'input'}),
            'cor': forms.TextInput(attrs={'class': 'input'}),
            'preco_custo': forms.NumberInput(attrs={'class': 'input', 'min': '0', 'step': '0.01'}),
            'preco_venda': forms.NumberInput(attrs={'class': 'input', 'min': '0', 'step': '0.01'}),
            'quantidade_estoque': forms.NumberInput(attrs={'class': 'input', 'min': '0', 'step': '1'}),
            'estoque_minimo': forms.NumberInput(attrs={'class': 'input', 'min': '0', 'step': '1'}),
        }
