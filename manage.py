#!/usr/bin/env python
"""Compatibilidade para comandos Django executados na raiz do repositório."""

import os
import sys
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
BACKEND_DIR = BASE_DIR / 'backend'
sys.path.insert(0, str(BACKEND_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# O projeto ainda usa o servidor de desenvolvimento do Django localmente.
# Sem esta opção, ele não entrega os scripts estáticos quando DEBUG=False.
if sys.argv[1:2] == ['runserver'] and '--insecure' not in sys.argv:
    sys.argv.insert(2, '--insecure')

from django.core.management import execute_from_command_line


if __name__ == '__main__':
    execute_from_command_line(sys.argv)
