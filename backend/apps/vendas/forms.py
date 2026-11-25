from django import forms
from django.forms import formset_factory

from apps.clientes.models import Cliente
from apps.produtos.models import Produto
from .models import Venda


class VendaForm(forms.Form):
    cliente = forms.ModelChoiceField(queryset=Cliente.objects.all(), required=False, empty_label='Consumidor não identificado', widget=forms.Select(attrs={'class': 'select'}))
    desconto_aplicado = forms.DecimalField(min_value=0, max_digits=10, decimal_places=2, initial=0, widget=forms.NumberInput(attrs={'class': 'input', 'min': '0', 'step': '0.01'}))
    forma_pagamento = forms.ChoiceField(choices=Venda.FormaPagamento.choices, widget=forms.Select(attrs={'class': 'select'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cliente'].label = 'Cliente'
        self.fields['desconto_aplicado'].label = 'Desconto em reais'
        self.fields['forma_pagamento'].label = 'Forma de pagamento'

    def clean(self):
        dados = super().clean()
        cliente = dados.get('cliente')
        forma = dados.get('forma_pagamento')
        if forma == Venda.FormaPagamento.FIADO and not cliente:
            self.add_error('cliente', 'Selecione um cliente para registrar uma venda fiado.')
        return dados


class ItemVendaForm(forms.Form):
    produto = forms.ModelChoiceField(
        queryset=Produto.objects.none(),
        empty_label='Selecione um produto',
        widget=forms.Select(attrs={'class': 'select'}),
    )
    quantidade = forms.IntegerField(
        required=False,
        min_value=1,
        widget=forms.NumberInput(attrs={'class': 'input', 'min': '1', 'step': '1'}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['produto'].queryset = Produto.objects.filter(ativo=True).order_by('nome_produto')
        self.fields['produto'].label = 'Produto'
        self.fields['quantidade'].label = 'Quantidade'

    def clean(self):
        dados = super().clean()
        if dados.get('produto') and dados.get('quantidade') is None:
            self.add_error('quantidade', 'Informe a quantidade do produto.')
        return dados


ItemVendaFormSet = formset_factory(ItemVendaForm, extra=5, max_num=12, validate_max=True)
