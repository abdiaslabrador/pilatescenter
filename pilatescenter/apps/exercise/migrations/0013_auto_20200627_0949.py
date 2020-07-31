# Generated by Django 3.0.7 on 2020-06-27 13:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('exercise', '0012_auto_20200623_1453'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hour',
            name='id_day_fk',
            field=models.ForeignKey(blank=True, db_column='id_day_fk', null=True, on_delete=django.db.models.deletion.CASCADE, to='exercise.Day'),
        ),
        migrations.AlterField(
            model_name='hour',
            name='id_exercise_fk',
            field=models.ForeignKey(blank=True, db_column='id_exercise_fk', null=True, on_delete=django.db.models.deletion.CASCADE, to='exercise.Exercise'),
        ),
    ]