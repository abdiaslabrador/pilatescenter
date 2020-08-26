from django.db import models
from apps.exercise.models import Exercise
from apps.create_user.models import CustomUser
from django.db.models import signals


# Create your models here.
class Lesson_det(models.Model):

	#is the value asign here is in capital case or not, is the way that appear in the database
	NOTONE		= 'NOTONE'
	OPEN		= 'OPEN'
	CLOSE		= 'CLOSE'
	NOTCHANCE 	= 'NOTCHANCE'
	INPROCESS 	= 'INPROCESS'
	FINISHED 	= 'FINISHED'
    

	lesson_status_choices = [
		(NOTONE, 'NOTONE'),
		(OPEN, 'OPEN'),
		(CLOSE, 'CLOSE'),
		(NOTCHANCE, 'NOTCHANCE'),
		(INPROCESS, 'INPROCESS'),
		(FINISHED, 'FINISHED'),
    ]

	lesson_status = models.CharField(
		max_length=10,
		choices=lesson_status_choices,
		default=NOTONE,
	)

	cant_max = models.IntegerField(default=0, null=True, blank=True)
	cant_in = models.IntegerField(default=0)
	quota 	= models.IntegerField(default=0)
	
	visible = models.BooleanField(default=True)
	enable 	= models.BooleanField(default=False)

	saw 	= models.BooleanField(default=False)

	day_lesson 	= models.DateField(null=True, blank=True)
	hour_chance =  models.TimeField(null=True, blank=True)
	hour_lesson =  models.TimeField(null=True, blank=True)
	hour_end 	=  models.TimeField(null=True, blank=True)

	id_user_fk = models.ManyToManyField(CustomUser, blank=True)
	id_exercise_fk = models.ForeignKey(Exercise, null=True, blank=True, on_delete=models.CASCADE, db_column='id_exercise_fk')
	
	def __str__(self):
		return str(self.id)

	#here i refresh the lesson status
	def custom_update_lesson(self):
		self.cant_in = self.id_user_fk.count()
		self.quota = self.cant_max - self.cant_in
		print("este es el estado de saw: " + str(self.saw))
		self.save()

