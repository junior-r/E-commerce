# Generated by Django 4.0.2 on 2022-05-18 22:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_producto_imagen'),
    ]

    operations = [
        migrations.AddField(
            model_name='producto',
            name='talla',
            field=models.CharField(blank=True, choices=[('S', 'S'), ('M', 'M'), ('X', 'X'), ('XL', 'XL'), ('XXL', 'XXL'), ('XXXL', 'XXXL')], max_length=5, null=True),
        ),
    ]
