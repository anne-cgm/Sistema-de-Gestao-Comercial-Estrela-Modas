from django.urls import path

from . import views


urlpatterns = [
    path('produtos/', views.produtos, name='produtos'),
    path('produtos/novo/', views.novo_produto, name='novo_produto'),
]
