from django.urls import path

from . import views


urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('relatorios/', views.relatorios, name='relatorios'),
]
