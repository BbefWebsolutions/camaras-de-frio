# Generated by Django 4.1.7 on 2023-03-12 18:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('appCamara', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='camara',
            options={'ordering': ['nombre'], 'verbose_name': 'Camara', 'verbose_name_plural': 'Camaras'},
        ),
    ]
