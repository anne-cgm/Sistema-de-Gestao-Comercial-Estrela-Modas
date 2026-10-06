from django.db import models

class Cliente(models.Model):
    nome = models.CharField(max_length=255)
    telefone = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        db_table = 'cliente'

    def __str__(self):
        return self.nome