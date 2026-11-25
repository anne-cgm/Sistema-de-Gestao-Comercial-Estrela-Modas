import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clientes', '0001_initial'),
        ('vendas', '0001_initial'),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            database_operations=[],
            state_operations=[
                migrations.CreateModel(
                    name='PagamentoDebito',
                    fields=[
                        ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                        ('valor', models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0.01)])),
                        ('data_pagamento', models.DateTimeField(auto_now_add=True)),
                        ('observacoes', models.CharField(blank=True, max_length=240)),
                        ('venda', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='pagamentos', to='vendas.venda')),
                    ],
                    options={
                        'verbose_name': 'Pagamento de débito',
                        'verbose_name_plural': 'Pagamentos de débitos',
                        'db_table': 'estrela_modas_pagamentodebito',
                    },
                ),
            ],
        ),
    ]
