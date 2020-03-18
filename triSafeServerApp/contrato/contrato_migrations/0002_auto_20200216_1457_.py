# Generated by Django 3.0 on 2020-02-16 17:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cliente', '0005_auto_20191214_1609'),
        ('contrato', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contrato',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_cliente_iter', models.IntegerField()),
                ('valorTotal', models.DecimalField(decimal_places=2, max_digits=10)),
                ('cliente', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='cliente.Cliente')),
            ],
        ),
        migrations.DeleteModel(
            name='Produto',
        ),
    ]
