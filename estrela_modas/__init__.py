"""Ponte de compatibilidade para o app Django em backend/estrela_modas."""

from pathlib import Path

BACKEND_DIR = Path(__file__).resolve().parent.parent / 'backend'
__path__.append(str(BACKEND_DIR / 'estrela_modas'))
