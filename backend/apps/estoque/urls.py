from django.urls import path

from . import views


urlpatterns = [
    # Telas autenticadas de consulta de estoque e registro de compras.
    path('estoque/', views.estoque, name='estoque'),
    path('compras/', views.compras, name='compras'),
]
