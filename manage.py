#!/usr/bin/env python
"""Compatibilidade para comandos Django executados na raiz do repositório."""

import os
import sys
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
BACKEND_DIR = BASE_DIR / 'backend'
sys.path.insert(0, str(BACKEND_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

from django.core.management import execute_from_command_line


if __name__ == '__main__':
    execute_from_command_line(sys.argv)
