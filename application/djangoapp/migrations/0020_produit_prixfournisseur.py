# Generated by Django 3.0.3 on 2020-02-04 15:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djangoapp', '0019_auto_20200204_1534'),
    ]

    operations = [
        migrations.AddField(
            model_name='produit',
            name='prixFournisseur',
            field=models.PositiveIntegerField(default=0),
        ),
    ]