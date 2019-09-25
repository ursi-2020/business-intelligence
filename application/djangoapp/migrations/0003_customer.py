# Generated by Django 2.2.5 on 2019-09-24 22:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djangoapp', '0002_adding_produit'),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstName', models.CharField(max_length=200)),
                ('lastName', models.CharField(max_length=200)),
                ('fidelityPoint', models.IntegerField(default=0)),
                ('payment', models.IntegerField(default=0)),
                ('account', models.CharField(default='', max_length=10)),
            ],
        ),
    ]
