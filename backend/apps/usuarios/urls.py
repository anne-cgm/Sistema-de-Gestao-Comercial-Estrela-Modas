from django.urls import path

from . import api, views


urlpatterns = [
    path('usuarios/', views.usuarios, name='usuarios'),
    path('api/usuarios/', api.api_usuarios, name='api_usuarios'),
    path('api/usuarios/permissoes-funcionarios/', api.api_permissoes_funcionarios, name='api_permissoes_funcionarios'),
    path('api/usuarios/<int:pk>/', api.api_usuario_detalhe, name='api_usuario_detalhe'),
]
