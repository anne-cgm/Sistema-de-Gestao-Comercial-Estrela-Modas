# Configurações de teste do Django

from .settings import *

DATABASES = {
    'default' : {
        'ENGINE': 'django.db.backends.sqlite3', # escolhe o SQLite como banco de dados para testes
        'NAME' : ':memory:', # mantém o banco de dados em memória, sem criar um arquivo de banco de projeto
    }
}



