# Generated by Django 3.0.4 on 2020-04-05 14:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('create_user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='username',
            field=models.CharField(blank=True, max_length=13, null=True),
        ),
    ]