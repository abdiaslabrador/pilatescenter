# Generated by Django 3.0.7 on 2020-12-09 18:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0004_auto_20201209_1423'),
    ]

    operations = [
        migrations.AddField(
            model_name='systempilates',
            name='cant_max',
            field=models.IntegerField(default=5),
        ),
    ]
