# Generated by Django 2.1.4 on 2019-01-19 19:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('WebApp', '0012_auto_20190119_1724'),
    ]

    operations = [
        migrations.AddField(
            model_name='uczestnikkursu',
            name='status_zapisu',
            field=models.CharField(choices=[('oczek', 'Oczekujące'), ('odrz', 'Odrzucone'), ('zaakc', 'Zaakceptowane')], default='oczek', max_length=255),
        ),
        migrations.AlterField(
            model_name='kurs',
            name='rodzaj_kursu',
            field=models.CharField(choices=[('skal', 'Kurs skałkowy'), ('tater', 'Kurs taternicki'), ('law', 'Kurs lawinowy')], max_length=255),
        ),
        migrations.AlterField(
            model_name='uczestnikkursu',
            name='potwierdzenie_wplaty',
            field=models.FileField(default='dddefault_val', upload_to='uploads'),
            preserve_default=False,
        ),
    ]
