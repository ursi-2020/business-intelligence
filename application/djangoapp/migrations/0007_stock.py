# Generated by Django 3.0 on 2019-12-13 10:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djangoapp', '0006_auto_20191202_0051'),
    ]

    operations = [
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(blank=True, null=True)),
                ('codeProduit', models.CharField(max_length=200)),
                ('quantite', models.IntegerField()),
            ],
        ),
    ]
