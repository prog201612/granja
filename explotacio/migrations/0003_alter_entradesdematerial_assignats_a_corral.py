# Generated by Django 4.2.5 on 2024-04-18 18:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('explotacio', '0002_comandesproveidor_detallcomandaproveidor_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entradesdematerial',
            name='assignats_a_corral',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=8),
        ),
    ]