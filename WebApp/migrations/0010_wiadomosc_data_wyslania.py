# Generated by Django 2.1.4 on 2019-01-18 23:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('WebApp', '0009_wiadomosc_przeczytana'),
    ]

    operations = [
        migrations.AddField(
            model_name='wiadomosc',
            name='data_wyslania',
            field=models.DateTimeField(auto_now_add=True, default='2019-01-19 00:10:12'),
            preserve_default=False,
        ),
    ]
