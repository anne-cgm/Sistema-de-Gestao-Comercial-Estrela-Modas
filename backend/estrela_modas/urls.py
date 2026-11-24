from django.urls import path
from . import views
from usuarios import api as usuarios_api

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_page, name='login'),
    path('recuperar-senha/', views.recuperar_senha, name='recuperar_senha'),
    path('redefinir-senha/<uidb64>/<token>/', views.redefinir_senha, name='redefinir_senha'),
    path('sair/', views.logout_page, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('produtos/', views.produtos, name='produtos'),
    path('produtos/novo/', views.novo_produto, name='novo_produto'),
    path('estoque/', views.estoque, name='estoque'),
    path('vendas/nova/', views.nova_venda, name='nova_venda'),
    path('clientes/', views.clientes, name='clientes'),
    path('clientes/<int:pk>/', views.cliente_detalhes, name='cliente_detalhes'),
    path('clientes/novo/', views.novo_cliente, name='novo_cliente'),
    path('debitos/', views.debitos, name='debitos'),
    path('mais/', views.mais_opcoes, name='mais_opcoes'),
    path('relatorios/', views.relatorios, name='relatorios'),
    path('compras/', views.compras, name='compras'),
    path('despesas/', views.despesas, name='despesas'),
    path('trocas/', views.trocas, name='trocas'),
    path('usuarios/', views.usuarios, name='usuarios'),
    path('api/usuarios/', usuarios_api.api_usuarios, name='api_usuarios'),
    path('api/usuarios/permissoes-funcionarios/', usuarios_api.api_permissoes_funcionarios, name='api_permissoes_funcionarios'),
    path('api/usuarios/<int:pk>/', usuarios_api.api_usuario_detalhe, name='api_usuario_detalhe'),
]
