# Generated by Django 4.0.2 on 2022-05-19 13:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_producto_talla'),
    ]

    operations = [
        migrations.CreateModel(
            name='Talla',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('talla', models.CharField(max_length=5)),
            ],
        ),
        migrations.RemoveField(
            model_name='producto',
            name='talla',
        ),
        migrations.AddField(
            model_name='producto',
            name='talla',
            field=models.ManyToManyField(related_name='Talla', to='app.Talla'),
        ),
    ]
