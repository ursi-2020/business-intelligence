# Generated by Gobrunk on 2020-01-17 14:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djangoapp', '0011_chiffre_affaire_benefice'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchasedarticle',
            name='Origin',
            field=models.CharField(default="rien", max_length=200),
        ),
    ]
