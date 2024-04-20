# Generated by Django 4.2.5 on 2024-04-19 07:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('explotacio', '0006_capacitatestoc_and_more'),
        ('globg', '0002_categoriacorral'),
    ]

    operations = [
        migrations.CreateModel(
            name='TipusProducte',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('actiu', models.BooleanField(default=True)),
                ('creat_el_dia', models.DateTimeField(auto_now_add=True)),
                ('modificat_el_dia', models.DateTimeField(auto_now=True)),
                ('nom', models.CharField(max_length=100)),
                ('tipus_capacitat', models.CharField(choices=[('co', 'Corral'), ('al', 'Aliment'), ('re', 'Rebuig')], max_length=2)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.DeleteModel(
            name='CategoriaCorral',
        ),
    ]