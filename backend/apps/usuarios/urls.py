from django.urls import path

from . import api, views


urlpatterns = [
    path('usuarios/', views.usuarios, name='usuarios'),
    path('api/usuarios/', api.api_usuarios, name='api_usuarios'),
    path('api/acesso-atual/', api.api_acesso_atual, name='api_acesso_atual'),
    path('api/usuarios/permissoes-funcionarios/', api.api_permissoes_funcionarios, name='api_permissoes_funcionarios'),
    path('api/usuarios/<int:pk>/codigo-recuperacao/', api.api_gerar_codigo_recuperacao, name='api_gerar_codigo_recuperacao'),
    path('api/usuarios/<int:pk>/', api.api_usuario_detalhe, name='api_usuario_detalhe'),
    path('api/recuperar-senha/', api.api_recuperar_senha_com_codigo, name='api_recuperar_senha_com_codigo'),
]
