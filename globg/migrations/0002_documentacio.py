# Generated by Django 4.2.5 on 2024-04-25 08:16

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('globg', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Documentacio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('actiu', models.BooleanField(default=True)),
                ('creat_el_dia', models.DateTimeField(auto_now_add=True)),
                ('modificat_el_dia', models.DateTimeField(auto_now=True)),
                ('nom', models.CharField(max_length=100)),
                ('descripcio', models.TextField()),
                ('caduca_el_dia', models.DateField(default=django.utils.timezone.now)),
                ('document', models.FileField(upload_to='documents/')),
            ],
            options={
                'verbose_name': 'Documentació',
                'verbose_name_plural': 'Documentacions',
                'ordering': ['nom'],
            },
        ),
    ]