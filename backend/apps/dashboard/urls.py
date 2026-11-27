from django.urls import path

from . import views


urlpatterns = [
    # Tela inicial com indicadores e filtros de período.
    path('dashboard/', views.dashboard, name='dashboard'),
    # Página de relatórios financeiros e operacionais.
    path('relatorios/', views.relatorios, name='relatorios'),
]
