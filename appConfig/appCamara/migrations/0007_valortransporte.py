# Generated by Django 4.1.7 on 2023-03-24 01:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appCamara', '0006_cotizacion_subneto_alter_camara_m2_alter_camara_m3_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ValorTransporte',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('valor', models.DecimalField(blank=True, decimal_places=2, default=None, max_digits=20, null=True, verbose_name='Valor x KM')),
                ('registroActivo', models.BooleanField(default=True, verbose_name='Registro Activo')),
                ('registroFechaCreacion', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Creación')),
                ('registroFechaModificacion', models.DateTimeField(auto_now=True, verbose_name='Fecha de\xa0Modificación')),
            ],
            options={
                'verbose_name': 'Valor KM',
                'verbose_name_plural': 'Valores KMs',
                'ordering': ['valor'],
            },
        ),
    ]
