# Generated by Django 3.0.2 on 2020-02-02 23:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djangoapp', '0012_ajout_origine'),
    ]

    operations = [
        migrations.CreateModel(
            name='Incident',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('client_id', models.TextField()),
                ('amount', models.IntegerField(default=0)),
                ('date', models.DateTimeField(blank=True, null=True)),
            ],
        ),
    ]
