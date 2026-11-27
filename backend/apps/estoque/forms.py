from django import forms

from apps.produtos.models import Produto


class CompraEntradaForm(forms.Form):
    """Valida os dados necessários para registrar uma entrada de compra."""

    # Só permitimos selecionar produtos ativos que já estejam cadastrados.
    produto = forms.ModelChoiceField(
        queryset=Produto.objects.none(),
        empty_label='Selecione um produto cadastrado',
        widget=forms.Select(attrs={'class': 'select', 'data-seletor-produto': ''}),
    )

    # A quantidade precisa ser positiva para representar uma entrada real.
    quantidade = forms.IntegerField(min_value=1, initial=1, widget=forms.NumberInput(attrs={
        'class': 'input', 'min': '1', 'step': '1',
    }))

    # O custo unitário é recebido como Decimal para evitar arredondamento de float.
    preco_custo_unitario = forms.DecimalField(min_value=0, max_digits=10, decimal_places=2,
        widget=forms.NumberInput(attrs={'class': 'input', 'min': '0', 'step': '0.01'}))

    # Fornecedor e nota fiscal são opcionais para compras feitas pela própria dona.
    fornecedor_nome = forms.CharField(required=False, max_length=160, widget=forms.TextInput(attrs={'class': 'input'}))
    numero_nota_fiscal = forms.CharField(required=False, max_length=64, widget=forms.TextInput(attrs={'class': 'input'}))

    def __init__(self, *args, **kwargs):
        """Limita o campo de produto aos itens ativos e define os rótulos da tela."""
        super().__init__(*args, **kwargs)
        self.fields['produto'].queryset = Produto.objects.filter(ativo=True).order_by('nome_produto')
        self.fields['fornecedor_nome'].label = 'Fornecedor'
        self.fields['numero_nota_fiscal'].label = 'Nota fiscal (opcional)'
        self.fields['quantidade'].label = 'Quantidade recebida'
        self.fields['preco_custo_unitario'].label = 'Preço de custo por unidade'

    def clean_fornecedor_nome(self):
        """Remove espaços para que fornecedor vazio seja salvo como string vazia."""
        return self.cleaned_data.get('fornecedor_nome', '').strip()

    def clean_numero_nota_fiscal(self):
        """Evita guardar apenas espaços como se houvesse uma nota fiscal."""
        return self.cleaned_data.get('numero_nota_fiscal', '').strip()
