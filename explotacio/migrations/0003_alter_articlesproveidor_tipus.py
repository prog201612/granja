# Generated by Django 4.2.5 on 2024-04-29 20:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('globg', '0003_alter_documentacio_descripcio_and_more'),
        ('explotacio', '0002_rename_preu_venta_articlesproveidor_preu_venda'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articlesproveidor',
            name='tipus',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='globg.tipusproducte'),
            preserve_default=False,
        ),
    ]
