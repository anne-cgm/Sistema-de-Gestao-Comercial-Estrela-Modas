from decimal import Decimal

from django import forms

from apps.vendas.models import Venda
from .models import Cliente, PagamentoDebito


class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nome_cliente', 'cpf_cliente', 'telefone', 'endereco_completo', 'limite_credito']
        labels = {
            'nome_cliente': 'Nome completo',
            'cpf_cliente': 'CPF (somente números)',
            'telefone': 'Telefone',
            'endereco_completo': 'Endereço',
            'limite_credito': 'Limite para compras fiado',
        }
        widgets = {
            'nome_cliente': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'Nome e sobrenome',
            }),
            'cpf_cliente': forms.TextInput(attrs={'class': 'input', 'inputmode': 'numeric', 'maxlength': '11'}),
            'telefone': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': '(00) 00000 - 0000',
                'inputmode': 'tel',
            }),
            'endereco_completo': forms.Textarea(attrs={'class': 'input', 'rows': 2}),
            'limite_credito': forms.NumberInput(attrs={'class': 'input', 'min': '0', 'step': '0.01'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cpf_cliente'].required = False
        self.fields['endereco_completo'].required = False
        self.fields['limite_credito'].required = False
        self.fields['limite_credito'].initial = Decimal('0.00')

    def clean_cpf_cliente(self):
        cpf = self.cleaned_data.get('cpf_cliente')
        if cpf is None or not str(cpf).strip():
            return None
        cpf = str(cpf).strip()
        if not cpf.isdigit() or len(cpf) != 11:
            raise forms.ValidationError('Informe os 11 números do CPF, sem pontuação.')
        return cpf

    def clean_limite_credito(self):
        limite = self.cleaned_data.get('limite_credito')
        return limite if limite is not None else Decimal('0.00')


class PagamentoDebitoForm(forms.ModelForm):
    class Meta:
        model = PagamentoDebito
        fields = ['venda', 'valor', 'observacoes']
        labels = {
            'venda': 'Dívida',
            'valor': 'Valor recebido',
            'observacoes': 'Observação',
        }
        widgets = {
            'venda': forms.Select(attrs={'class': 'select'}),
            'valor': forms.NumberInput(attrs={
                'class': 'input',
                'min': '0.01',
                'step': '0.01',
            }),
            'observacoes': forms.TextInput(attrs={'class': 'input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['venda'].queryset = (
            Venda.objects
            .filter(forma_pagamento=Venda.FormaPagamento.FIADO)
            .select_related('cliente')
            .order_by('-data_venda')
        )
        self.fields['venda'].empty_label = 'Selecione uma dívida'
        self.fields['venda'].label_from_instance = self.label_from_instance

    def label_from_instance(self, venda):
        cliente = venda.cliente.nome_cliente if venda.cliente else 'Cliente não informado'
        return (
            f'Venda #{venda.id} - {cliente} - '
            f'{venda.data_venda:%d/%m/%Y %H:%M} - '
            f'Saldo: R$ {venda.saldo_devedor:.2f}'
        )

    def clean(self):
        dados = super().clean()
        venda = dados.get('venda')
        valor = dados.get('valor')
        if venda and valor:
            if venda.forma_pagamento != Venda.FormaPagamento.FIADO:
                self.add_error('venda', 'Selecione uma venda fiada.')
            elif venda.saldo_devedor <= 0:
                self.add_error('venda', 'Essa dívida já está quitada.')
            elif valor > venda.saldo_devedor:
                self.add_error('valor', 'O pagamento não pode ser maior que o saldo dessa dívida.')
        return dados
