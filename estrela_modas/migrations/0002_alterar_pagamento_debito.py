from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('estrela_modas', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pagamentodebito',
            name='cliente',
        ),
        migrations.AddField(
            model_name='pagamentodebito',
            name='venda',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name='pagamentos',
                to='estrela_modas.venda',
            ),
        ),
    ]