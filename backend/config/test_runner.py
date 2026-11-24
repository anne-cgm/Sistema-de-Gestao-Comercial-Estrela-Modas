from pathlib import Path

from django.apps import apps
from django.conf import settings
from django.test.runner import DiscoverRunner


class AppTestDiscoverRunner(DiscoverRunner):
    """Descobre os módulos de teste guardados dentro dos apps locais."""

    def build_suite(self, test_labels=None, **kwargs):
        if not test_labels:
            raiz_backend = Path(settings.BASE_DIR) / 'backend'
            test_labels = []
            for app_config in apps.get_app_configs():
                caminho_app = Path(app_config.path)
                if not caminho_app.is_relative_to(raiz_backend):
                    continue
                test_labels.extend(
                    f'{app_config.name}.{arquivo.stem}'
                    for arquivo in sorted(caminho_app.glob('test*.py'))
                )
        return super().build_suite(test_labels=test_labels, **kwargs)
