# Generated by Django 3.0.7 on 2020-06-14 18:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exercise', '0003_exercise_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exercise',
            name='description',
            field=models.TextField(blank=True, default='', null=True),
        ),
    ]