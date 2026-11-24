"""Ponte de compatibilidade para o pacote de configuração em backend/config."""

from pathlib import Path

BACKEND_DIR = Path(__file__).resolve().parent.parent / 'backend'
__path__.append(str(BACKEND_DIR / 'config'))
