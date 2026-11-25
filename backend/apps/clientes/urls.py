from django.urls import path

from . import views


urlpatterns = [
    path('clientes/', views.clientes, name='clientes'),
    path('clientes/<int:pk>/', views.cliente_detalhes, name='cliente_detalhes'),
    path('clientes/novo/', views.novo_cliente, name='novo_cliente'),
    path('debitos/', views.debitos, name='debitos'),
]
