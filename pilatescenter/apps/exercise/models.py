from django.db import models


class Exercise(models.Model):
	name  	     = models.CharField(max_length=64)
	description  = models.TextField(null=True, blank=True)
	is_active    = models.BooleanField(default=False)


	def __str__(self):
		return self.name + str(self.id)

	def save(self, *args, **kwargs):
		self.name = self.name.upper()
		super(Exercise, self).save(*args, **kwargs)

class Day(models.Model):
	name = models.CharField(max_length=28)
	

	def __str__(self):
		return str(self.name)

class Hour(models.Model):
	hour_chance =  models.TimeField(null=False, blank=False)
	hour_lesson =  models.TimeField(null=False, blank=False)
	hour_end 	=  models.TimeField(null=False, blank=False)

	id_exercise_fk = models.ForeignKey(Exercise, null=True, blank=True, on_delete=models.CASCADE, db_column='id_exercise_fk')
	id_day_fk = models.ForeignKey(Day, null=True, blank=True, on_delete=models.CASCADE, db_column='id_day_fk')

	def __str__(self):
		# return str(self.id_exercise_fk) + str(self.id_day_fk)
		return "Chance:" + str(self.hour_chance) + "----Leccion:" + str(self.hour_lesson) + "----Final:" + str(self.hour_end)
