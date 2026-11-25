from decimal import Decimal

from django import forms
from django.db.models import DecimalField, F, Sum, Value
from django.db.models.functions import Coalesce
from django.utils import timezone

from apps.vendas.models import Venda
from .models import Cliente, PagamentoDebito


class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nome_cliente', 'telefone']
        labels = {
            'nome_cliente': 'Nome completo',
            'telefone': 'Telefone',
        }
        widgets = {
            'nome_cliente': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'Nome e sobrenome',
                'required': 'True'
            }),
            'telefone': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': '(00) 00000 - 0000',
                'inputmode': 'tel',
                'required': 'True'
            }),
        }

# Associa pagamentos diretamente à venda, permitindo o cálculo correto do saldo devedor e da situação do débito.
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
            .annotate(
                total_pago_calculado=Coalesce(
                    Sum('pagamentos__valor'),
                    Value(Decimal('0.00')),
                    output_field=DecimalField(max_digits=12, decimal_places=2),
                )
            )
            .filter(total_pago_calculado__lt=F('valor_total'))
            .select_related('cliente')
            .order_by('-data_venda')
        )
        self.fields['venda'].empty_label = 'Selecione uma dívida'

        # Define como cada venda aparecerá no campo de seleção, incluindo o nome do cliente, a data da venda e o saldo devedor.
        self.fields['venda'].label_from_instance = self.label_from_instance

    def label_from_instance(self, venda):
        cliente = venda.cliente.nome_cliente if venda.cliente else 'Cliente não informado'
        data_venda_local = timezone.localtime(
            venda.data_venda,
            timezone.get_default_timezone(),
        )
        return (
            f'Venda #{venda.id} - {cliente} - '
            f'{data_venda_local:%d/%m/%Y %H:%M} - '
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
