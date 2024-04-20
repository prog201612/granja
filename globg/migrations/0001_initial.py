# Generated by Django 4.2.5 on 2024-04-18 15:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Explotacio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('actiu', models.BooleanField(default=True)),
                ('creat_el_dia', models.DateTimeField(auto_now_add=True)),
                ('modificat_el_dia', models.DateTimeField(auto_now=True)),
                ('nom', models.CharField(max_length=100)),
                ('descripcio', models.TextField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PersonaLegal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('actiu', models.BooleanField(default=True)),
                ('creat_el_dia', models.DateTimeField(auto_now_add=True)),
                ('modificat_el_dia', models.DateTimeField(auto_now=True)),
                ('nom', models.CharField(max_length=100)),
                ('dni_nif', models.CharField(max_length=20)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Telefon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('actiu', models.BooleanField(default=True)),
                ('creat_el_dia', models.DateTimeField(auto_now_add=True)),
                ('modificat_el_dia', models.DateTimeField(auto_now=True)),
                ('telefon', models.CharField(max_length=20, verbose_name='Telèfon')),
                ('descripcio', models.CharField(max_length=100, verbose_name='Descripció')),
                ('persona_legal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='globg.personalegal')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Email',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('actiu', models.BooleanField(default=True)),
                ('creat_el_dia', models.DateTimeField(auto_now_add=True)),
                ('modificat_el_dia', models.DateTimeField(auto_now=True)),
                ('email', models.EmailField(max_length=254)),
                ('descripcio', models.CharField(max_length=100, verbose_name='Descripció')),
                ('persona_legal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='globg.personalegal')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
