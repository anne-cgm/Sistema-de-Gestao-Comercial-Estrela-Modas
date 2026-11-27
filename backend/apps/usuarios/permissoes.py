"""Regras compartilhadas para o acesso dos funcionários às páginas."""

from functools import wraps

from django.contrib import messages
from django.shortcuts import redirect

from .models import ConfiguracaoPermissoesFuncionarios


# Chaves estáveis usadas pela tela de permissões, pelo menu e pelas views.
PAGINAS_PERMITIDAS = (
    {'chave': 'dashboard', 'nome': 'Dashboard', 'descricao': 'Indicadores e resumo da loja.'},
    {'chave': 'produtos', 'nome': 'Produtos', 'descricao': 'Catálogo e cadastro de produtos.'},
    {'chave': 'estoque', 'nome': 'Estoque', 'descricao': 'Consulta de quantidades e reposição.'},
    {'chave': 'compras', 'nome': 'Compras', 'descricao': 'Registro de compras e entradas.'},
    {'chave': 'vendas', 'nome': 'Vendas', 'descricao': 'Registro de vendas.'},
    {'chave': 'clientes', 'nome': 'Clientes', 'descricao': 'Cadastro e consulta de clientes.'},
    {'chave': 'debitos', 'nome': 'Débitos', 'descricao': 'Consulta de débitos e pagamentos.'},
    {'chave': 'trocas', 'nome': 'Trocas', 'descricao': 'Registro e consulta de trocas.'},
    {'chave': 'despesas', 'nome': 'Despesas', 'descricao': 'Registro de despesas da loja.'},
    {'chave': 'relatorios', 'nome': 'Relatórios', 'descricao': 'Resumo e relatórios do sistema.'},
)
PERMISSOES_DISPONIVEIS = frozenset(pagina['chave'] for pagina in PAGINAS_PERMITIDAS)


def permissoes_ativas_do_funcionario():
    """Retorna a seleção atual do administrador; sem configuração, ninguém recebe acesso extra."""
    permissoes = (
        ConfiguracaoPermissoesFuncionarios.objects
        .filter(pk=1)
        .values_list('permissoes', flat=True)
        .first()
    )
    return set(permissoes or [])


def exigir_permissao(chave):
    """Bloqueia no servidor a página quando o funcionário não tem a permissão marcada."""
    if chave not in PERMISSOES_DISPONIVEIS:
        raise ValueError(f'Permissão não cadastrada: {chave}')

    def decorar(view):
        @wraps(view)
        def verificar_acesso(request, *args, **kwargs):
            # Administradores mantêm acesso total e não dependem do checklist.
            if request.user.is_superuser or chave in permissoes_ativas_do_funcionario():
                return view(request, *args, **kwargs)

            messages.error(request, 'Seu perfil não tem acesso a esta página. Peça autorização ao administrador da loja.')
            return redirect('mais_opcoes')

        return verificar_acesso

    return decorar
