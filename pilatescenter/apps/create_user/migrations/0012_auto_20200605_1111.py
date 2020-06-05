# Generated by Django 3.0.6 on 2020-06-05 15:11

import apps.create_user.validators
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('create_user', '0011_exercise_det'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='username',
            field=models.CharField(default="Ninguno", max_length=28, unique=True, validators=[apps.create_user.validators.name_space]),
            preserve_default=False,
        ),
    ]
