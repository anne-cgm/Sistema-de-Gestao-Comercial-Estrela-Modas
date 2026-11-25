from django import forms

from apps.produtos.models import Produto
from apps.vendas.models import Venda
from .models import Troca


class TrocaForm(forms.ModelForm):
    class Meta:
        model = Troca
        fields = ['venda', 'produto_devolvido', 'produto_entregue', 'motivo_troca', 'cupom_credito']
        labels = {
            'venda': 'Venda de origem (opcional)',
            'produto_devolvido': 'Produto devolvido',
            'produto_entregue': 'Produto entregue (opcional)',
            'motivo_troca': 'Motivo da troca',
            'cupom_credito': 'Crédito gerado',
        }
        widgets = {
            'venda': forms.Select(attrs={'class': 'select'}),
            'produto_devolvido': forms.Select(attrs={'class': 'select'}),
            'produto_entregue': forms.Select(attrs={'class': 'select'}),
            'motivo_troca': forms.Textarea(attrs={'class': 'input', 'rows': 2}),
            'cupom_credito': forms.NumberInput(attrs={'class': 'input', 'min': '0', 'step': '0.01'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['venda'].queryset = Venda.objects.order_by('-data_venda')
        self.fields['produto_devolvido'].queryset = Produto.objects.filter(ativo=True)
        self.fields['produto_entregue'].queryset = Produto.objects.filter(ativo=True)
        self.fields['produto_entregue'].required = False
        self.fields['venda'].empty_label = 'Selecione uma venda (opcional)'
        self.fields['produto_devolvido'].empty_label = 'Selecione o produto devolvido'
        self.fields['produto_entregue'].empty_label = 'Selecione o produto entregue'

    def clean(self):
        dados = super().clean()
        if dados.get('produto_entregue') and dados.get('produto_entregue') == dados.get('produto_devolvido'):
            self.add_error('produto_entregue', 'Escolha um produto diferente do que foi devolvido.')
        return dados
