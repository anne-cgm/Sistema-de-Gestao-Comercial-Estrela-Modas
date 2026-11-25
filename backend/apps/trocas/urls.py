from django.urls import path

from . import views


urlpatterns = [
    path('trocas/', views.trocas, name='trocas'),
]
