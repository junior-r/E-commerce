# Generated by Django 4.0.2 on 2022-05-19 14:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_talla_remove_producto_talla_producto_talla'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='talla',
            options={'ordering': ('id',)},
        ),
    ]
