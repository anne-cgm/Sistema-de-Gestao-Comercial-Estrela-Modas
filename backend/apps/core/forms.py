from django import forms

from .models import Despesa


CATEGORIAS_DESPESA = [
    ('operacional', 'Operacional'),
    ('viagem', 'Viagem'),
    ('marketing', 'Marketing'),
    ('aluguel', 'Aluguel'),
    ('servicos', 'Serviços'),
    ('outros', 'Outros'),
]


class DespesaForm(forms.ModelForm):
    categoria_despesa = forms.ChoiceField(
        choices=CATEGORIAS_DESPESA,
        widget=forms.Select(attrs={'class': 'select'}),
    )

    class Meta:
        model = Despesa
        fields = [
            'descricao_despesa',
            'categoria_despesa',
            'valor_despesa',
            'data_despesa',
            'observacoes',
        ]
        labels = {
            'descricao_despesa': 'Descrição',
            'categoria_despesa': 'Categoria',
            'valor_despesa': 'Valor',
            'data_despesa': 'Data',
            'observacoes': 'Observações',
        }
        widgets = {
            'descricao_despesa': forms.TextInput(attrs={'class': 'input'}),
            'valor_despesa': forms.NumberInput(attrs={
                'class': 'input',
                'min': '0.01',
                'step': '0.01',
            }),
            'data_despesa': forms.DateInput(attrs={'class': 'input', 'type': 'date'}),
            'observacoes': forms.Textarea(attrs={'class': 'input', 'rows': 2}),
        }
