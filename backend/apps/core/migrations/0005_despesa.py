import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('estrela_modas', '0004_remove_venda_cliente_remove_itemcompra_compra_and_more'),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            database_operations=[],
            state_operations=[
                migrations.CreateModel(
                    name='Despesa',
                    fields=[
                        ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                        ('descricao_despesa', models.CharField(max_length=180)),
                        ('categoria_despesa', models.CharField(max_length=80)),
                        ('valor_despesa', models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0.01)])),
                        ('data_despesa', models.DateField()),
                        ('observacoes', models.TextField(blank=True)),
                    ],
                    options={
                        'verbose_name': 'despesa',
                        'verbose_name_plural': 'despesas',
                        'db_table': 'estrela_modas_despesa',
                        'ordering': ['-data_despesa'],
                    },
                ),
            ],
        ),
    ]
