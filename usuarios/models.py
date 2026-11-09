from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


class UsuarioManager(BaseUserManager):
    def create_user(self, login, email=None, password=None, **extra_fields):
        if not login:
            raise ValueError('O usuário deve ter um login.')
        
        email = self.normalize_email(email) if email else email
        user = self.model(login=login, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, login, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superusuario deve ter is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superusuario deve ter is_superuser=True.')

        return self.create_user(login, email, password, **extra_fields)


class Usuario(AbstractUser):
    username = None  # Remove o campo 'username' padrão do AbstractUser

    nome = models.CharField(max_length=255)
    login = models.CharField(max_length=100, unique=True)
    ativo = models.BooleanField(default=True)

    USERNAME_FIELD = 'login'
    REQUIRED_FIELDS = ['nome', 'email']

    objects = UsuarioManager()

    class Meta:
        db_table = 'usuario'

    def __str__(self):
        return f"{self.nome} ({self.login})"