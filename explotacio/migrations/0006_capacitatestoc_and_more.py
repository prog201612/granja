# Generated by Django 4.2.5 on 2024-04-19 07:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('explotacio', '0005_capacitat'),
    ]

    operations = [
        migrations.CreateModel(
            name='CapacitatEstoc',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('actiu', models.BooleanField(default=True)),
                ('creat_el_dia', models.DateTimeField(auto_now_add=True)),
                ('modificat_el_dia', models.DateTimeField(auto_now=True)),
                ('quantitat', models.DecimalField(decimal_places=2, max_digits=8)),
            ],
            options={
                'verbose_name': "Capacitat d'estoc",
                'verbose_name_plural': "Capacitats d'estoc",
                'ordering': ['capacitat__tipus', 'capacitat__capacitat'],
            },
        ),
        migrations.RemoveField(
            model_name='articlesproveidor',
            name='categoria_corral',
        ),
    ]