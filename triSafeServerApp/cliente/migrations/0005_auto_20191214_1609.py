# Generated by Django 3.0 on 2019-12-14 19:09

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('cliente', '0004_cliente_id_cliente_iter'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cliente',
            old_name='endereco',
            new_name='rua',
        ),
        migrations.RenameField(
            model_name='cliente',
            old_name='estado',
            new_name='uf',
        ),
        migrations.AddField(
            model_name='cliente',
            name='numero',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='cliente',
            name='senha',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='cliente',
            name='senhaConfirmacao',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='cliente',
            name='dt_hr_inclusao',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
