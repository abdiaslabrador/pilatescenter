from django.db import models
from apps.exercise.models import Exercise
from apps.create_user.models import CustomUser



class Hour(models.Model):
	hour_chance =  models.TimeField(null=True, blank=True)
	hour_lesson =  models.TimeField(null=True, blank=True)
	hour_end 	=  models.TimeField(null=True, blank=True)

	id_exercise_fk = models.ForeignKey(Exercise, null=True, blank=True, on_delete=models.CASCADE, db_column='id_exercise_fk')

	def __str__(self):
		return str(self.hour_lesson) + "   "+ str(self.id_exercise_fk)

# Create your models here.
class Lesson_det(models.Model):
	cant_max = models.IntegerField(default=0)
	cant_in = models.IntegerField(default=0)
	quota 	= models.IntegerField(default=0)
	visible = models.BooleanField(default=True)
	enable 	= models.BooleanField(default=True)

	hour_lesson = models.TimeField(null=True, blank=True,)

	id_user_fk 	= models.ManyToManyField(CustomUser)
	id_exercise_fk = models.ForeignKey(Exercise, null=True, blank=True, on_delete=models.CASCADE, db_column='id_exercise_fk')
	
	def __str__(self):
		return "Clase nº: " + str(self.id)

