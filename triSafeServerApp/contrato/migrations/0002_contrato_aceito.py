# Generated by Django 3.0 on 2020-04-01 01:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contrato', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='contrato',
            name='aceito',
            field=models.BooleanField(default=False),
        ),
    ]
