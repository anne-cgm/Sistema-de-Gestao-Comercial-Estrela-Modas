from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.core.urls')),
    path('', include('apps.dashboard.urls')),
    path('', include('apps.usuarios.urls')),
    path('', include('apps.produtos.urls')),
    path('', include('apps.clientes.urls')),
    path('', include('apps.vendas.urls')),
    path('', include('apps.estoque.urls')),
    path('', include('apps.trocas.urls')),
]
