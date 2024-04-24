# Generated by Django 4.2.5 on 2024-04-24 10:29

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='detallvenda',
            name='preu_venda',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=8),
        ),
        migrations.AlterField(
            model_name='detallvenda',
            name='quantitat',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=8),
        ),
        migrations.AlterField(
            model_name='vendes',
            name='data_venta',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
