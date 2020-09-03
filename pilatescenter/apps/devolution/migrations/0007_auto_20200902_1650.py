# Generated by Django 3.0.7 on 2020-09-02 20:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('exercise', '0013_auto_20200627_0949'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('devolution', '0006_auto_20200902_1648'),
    ]

    operations = [
        migrations.AlterField(
            model_name='devolution',
            name='id_exercise_fk',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='exercise.Exercise'),
        ),
        migrations.AlterField(
            model_name='devolution',
            name='id_user_fk',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]