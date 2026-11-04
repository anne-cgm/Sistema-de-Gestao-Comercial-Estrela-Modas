from django import forms
from django.forms import formset_factory

from .models import Cliente, Despesa, PagamentoDebito, Produto, Troca, Venda


class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = [
            'nome_produto', 'sku', 'categoria', 'tamanho', 'cor',
            'preco_custo', 'preco_venda', 'quantidade_estoque', 'estoque_minimo',
        ]
        labels = {
            'nome_produto': 'Nome do produto',
            'sku': 'SKU',
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


class CompraEntradaForm(forms.Form):
    produto = forms.ModelChoiceField(
        queryset=Produto.objects.none(),
        empty_label='Selecione um produto cadastrado',
        widget=forms.Select(attrs={'class': 'select', 'data-seletor-produto': ''}),
    )
    quantidade = forms.IntegerField(min_value=1, initial=1, widget=forms.NumberInput(attrs={
        'class': 'input', 'min': '1', 'step': '1',
    }))
    preco_custo_unitario = forms.DecimalField(min_value=0, max_digits=10, decimal_places=2,
        widget=forms.NumberInput(attrs={'class': 'input', 'min': '0', 'step': '0.01'}))
    fornecedor_nome = forms.CharField(required=False, max_length=160, widget=forms.TextInput(attrs={'class': 'input'}))
    numero_nota_fiscal = forms.CharField(required=False, max_length=64, widget=forms.TextInput(attrs={'class': 'input'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['produto'].queryset = Produto.objects.filter(ativo=True).order_by('nome_produto')
        self.fields['fornecedor_nome'].label = 'Fornecedor'
        self.fields['numero_nota_fiscal'].label = 'Nota fiscal (opcional)'
        self.fields['quantidade'].label = 'Quantidade recebida'
        self.fields['preco_custo_unitario'].label = 'Preço de custo por unidade'


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
            'nome_cliente': forms.TextInput(attrs={'class': 'input'}),
            'cpf_cliente': forms.TextInput(attrs={'class': 'input', 'inputmode': 'numeric', 'maxlength': '11'}),
            'telefone': forms.TextInput(attrs={'class': 'input'}),
            'endereco_completo': forms.Textarea(attrs={'class': 'input', 'rows': 2}),
            'limite_credito': forms.NumberInput(attrs={'class': 'input', 'min': '0', 'step': '0.01'}),
        }

    def clean_cpf_cliente(self):
        cpf = self.cleaned_data.get('cpf_cliente', '').strip()
        if not cpf:
            return None
        if not cpf.isdigit() or len(cpf) != 11:
            raise forms.ValidationError('Informe os 11 números do CPF, sem pontuação.')
        return cpf


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
    produto = forms.ModelChoiceField(queryset=Produto.objects.none(), widget=forms.Select(attrs={'class': 'select'}))
    quantidade = forms.IntegerField(min_value=1, initial=1, widget=forms.NumberInput(attrs={'class': 'input', 'min': '1', 'step': '1'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['produto'].queryset = Produto.objects.filter(ativo=True).order_by('nome_produto')
        self.fields['produto'].label = 'Produto'
        self.fields['quantidade'].label = 'Quantidade'


ItemVendaFormSet = formset_factory(ItemVendaForm, extra=5, max_num=12, validate_max=True)


class PagamentoDebitoForm(forms.ModelForm):
    class Meta:
        model = PagamentoDebito
        fields = ['cliente', 'valor', 'observacoes']
        labels = {'cliente': 'Cliente', 'valor': 'Valor recebido', 'observacoes': 'Observação'}
        widgets = {
            'cliente': forms.Select(attrs={'class': 'select'}),
            'valor': forms.NumberInput(attrs={'class': 'input', 'min': '0.01', 'step': '0.01'}),
            'observacoes': forms.TextInput(attrs={'class': 'input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cliente'].queryset = Cliente.objects.order_by('nome_cliente')

    def clean(self):
        dados = super().clean()
        cliente = dados.get('cliente')
        valor = dados.get('valor')
        if cliente and valor and valor > cliente.saldo_devedor:
            self.add_error('valor', 'O pagamento não pode ser maior que o débito atual.')
        return dados


class DespesaForm(forms.ModelForm):
    class Meta:
        model = Despesa
        fields = ['descricao_despesa', 'categoria_despesa', 'valor_despesa', 'data_despesa', 'observacoes']
        labels = {
            'descricao_despesa': 'Descrição',
            'categoria_despesa': 'Categoria',
            'valor_despesa': 'Valor',
            'data_despesa': 'Data',
            'observacoes': 'Observações',
        }
        widgets = {
            'descricao_despesa': forms.TextInput(attrs={'class': 'input'}),
            'categoria_despesa': forms.TextInput(attrs={'class': 'input'}),
            'valor_despesa': forms.NumberInput(attrs={'class': 'input', 'min': '0.01', 'step': '0.01'}),
            'data_despesa': forms.DateInput(attrs={'class': 'input', 'type': 'date'}),
            'observacoes': forms.Textarea(attrs={'class': 'input', 'rows': 2}),
        }


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

    def clean(self):
        dados = super().clean()
        if dados.get('produto_entregue') and dados.get('produto_entregue') == dados.get('produto_devolvido'):
            self.add_error('produto_entregue', 'Escolha um produto diferente do que foi devolvido.')
        return dados
