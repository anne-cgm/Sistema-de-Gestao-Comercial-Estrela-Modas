from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0003_alter_usuario_managers'),
    ]

    operations = [
        migrations.CreateModel(
            name='ConfiguracaoPermissoesFuncionarios',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('permissoes', models.JSONField(default=list)),
                ('atualizado_em', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'configuração de permissões dos funcionários',
                'verbose_name_plural': 'configurações de permissões dos funcionários',
            },
        ),
    ]
