from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static


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
]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
