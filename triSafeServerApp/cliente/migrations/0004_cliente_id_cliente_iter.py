# Generated by Django 2.2.1 on 2019-11-26 00:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cliente', '0003_remove_cliente_salario'),
    ]

    operations = [
        migrations.AddField(
            model_name='cliente',
            name='id_cliente_iter',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]