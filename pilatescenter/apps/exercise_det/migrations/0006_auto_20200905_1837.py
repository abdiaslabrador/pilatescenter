# Generated by Django 3.0.7 on 2020-09-05 22:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('exercise', '0013_auto_20200627_0949'),
        ('exercise_det', '0005_exercise_det_devolutions'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exercise_det',
            name='id_exercise_fk',
            field=models.ForeignKey(db_column='id_exercise_fk', on_delete=django.db.models.deletion.CASCADE, to='exercise.Exercise'),
        ),
    ]
