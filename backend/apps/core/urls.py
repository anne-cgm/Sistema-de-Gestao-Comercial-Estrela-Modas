from django.urls import path

from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_page, name='login'),
    path('recuperar-senha/', views.recuperar_senha, name='recuperar_senha'),
    path('redefinir-senha/<uidb64>/<token>/', views.redefinir_senha, name='redefinir_senha'),
    path('sair/', views.logout_page, name='logout'),
    path('mais/', views.mais_opcoes, name='mais_opcoes'),
    path('despesas/', views.despesas, name='despesas'),
]
