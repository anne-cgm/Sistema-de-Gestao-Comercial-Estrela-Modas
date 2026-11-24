#!/usr/bin/env python
"""Utilitário de linha de comando do Django para o backend."""

import os
import sys


def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    if sys.argv[1:2] == ['runserver'] and '--insecure' not in sys.argv:
        sys.argv.insert(2, '--insecure')
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
