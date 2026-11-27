from django.apps import AppConfig


class DashboardConfig(AppConfig):
    """Configuração da aplicação de dashboard e relatórios."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.dashboard'
    verbose_name = 'Painel e relatórios'
