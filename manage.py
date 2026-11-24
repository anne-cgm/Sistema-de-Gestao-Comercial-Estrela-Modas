#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    # O runserver é usado somente no desenvolvimento local neste projeto.
    # Garante os arquivos de frontend quando DEBUG estiver desativado por ambiente.
    if len(sys.argv) > 1 and sys.argv[1] == 'runserver' and '--insecure' not in sys.argv:
        sys.argv.insert(2, '--insecure')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
