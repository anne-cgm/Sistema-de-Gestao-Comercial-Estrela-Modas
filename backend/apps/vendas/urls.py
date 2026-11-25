from django.urls import path

from . import views


urlpatterns = [
    path('vendas/nova/', views.nova_venda, name='nova_venda'),
]
