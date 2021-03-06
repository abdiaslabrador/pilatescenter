# Generated by Django 3.0.7 on 2020-09-01 05:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('exercise', '0013_auto_20200627_0949'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('lesson_det', '0026_auto_20200901_0110'),
    ]

    operations = [
        migrations.CreateModel(
            name='Devolution',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day_lesson', models.DateField(blank=True, null=True)),
                ('hour_chance', models.TimeField(blank=True, null=True)),
                ('hour_lesson', models.TimeField(blank=True, null=True)),
                ('hour_end', models.TimeField(blank=True, null=True)),
                ('selected', models.BooleanField(default=False)),
                ('returned', models.BooleanField(default=False)),
                ('id_exercise_fk', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='exercise.Exercise')),
                ('id_lesson_fk', models.ManyToManyField(blank=True, to='lesson_det.Lesson_det')),
                ('id_user_fk', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
