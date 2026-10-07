from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_page, name='login'),
    path('sair/', views.logout_page, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('produtos/', views.produtos, name='produtos'),
    path('produtos/novo/', views.cadastro_produto, name='cadastro_produto'),
    path('estoque/', views.estoque, name='estoque'),
    path('vendas/nova/', views.nova_venda, name='nova_venda'),
    path('clientes/', views.clientes, name='clientes'),
    path('debitos/', views.debitos, name='debitos'),
    path('mais/', views.mais_opcoes, name='mais_opcoes'),
    path('relatorios/', views.relatorios, name='relatorios'),
    path('compras/', views.compras, name='compras'),
    path('despesas/', views.despesas, name='despesas'),
    path('trocas/', views.trocas, name='trocas'),
]
