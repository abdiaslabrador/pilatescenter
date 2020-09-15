from django.db import models
from apps.exercise.models import Exercise
from apps.create_user.models import CustomUser
from apps.lesson_det.models import Lesson_det



class Devolution(models.Model):

	id_lesson_before = models.IntegerField(default=0)
	
	day_lesson 	= models.DateField(null=True, blank=True)
	hour_chance =  models.TimeField(null=True, blank=True)
	hour_lesson =  models.TimeField(null=True, blank=True)
	hour_end 	=  models.TimeField(null=True, blank=True)

	returned = models.BooleanField(default=False)

	cant_max = models.IntegerField(default=0, null=True, blank=True)
	cant_in = models.IntegerField(default=0)

	id_lesson_fk = models.ManyToManyField(Lesson_det, blank=True)
	id_user_fk = models.ForeignKey(CustomUser,  on_delete=models.CASCADE)
	id_exercise_fk = models.ForeignKey(Exercise,  on_delete=models.CASCADE)