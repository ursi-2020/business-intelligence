# Generated by Django 3.0.2 on 2020-02-03 10:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djangoapp', '0012_ajout_origine'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='purchasedarticle',
            name='Origin',
        ),
        migrations.AddField(
            model_name='ticket',
            name='Origin',
            field=models.CharField(default='rien', max_length=200),
        ),
    ]