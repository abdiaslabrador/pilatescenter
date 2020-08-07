from django.db import models
from apps.exercise.models import Exercise


# class pilatesManager(models.Manager):
# 	def pilates(self):
# 		return Plan.objects.filter(id_exercise_fk__name__iexact='pilates')
# 	def yoga(self):
# 		return Plan.objects.filter(id_exercise_fk__name__iexact='yoga')

# 	def hot_pilates(self):
# 		return Plan.objects.filter(id_exercise_fk__name__iexact='hot pilates')


class Plan(models.Model):

	"""
		hay un signal pre_delete en el modelo Exercise_det, que hace que al ser eliminado un plan
		le asigna el plan "ninguno" a la relaciòn id_exercise_fk"""

	"""
		default attribute of 'description' not works with textfield(),
		but that attribute asign to it a not null value in the database,
		because of that i can manipulate it to asign a default value later in the see_plan.html
	"""

	name 			= models.CharField(null=False, blank=False, max_length=64)
	total_days		= models.IntegerField(null=False, blank=False, default=0)
	oportunities	= models.IntegerField(null=False, blank=False, default=0)
	description 	= models.TextField(null=True, blank=True)


	id_exercise_fk = models.ForeignKey(Exercise, null=True, blank=False, on_delete=models.CASCADE, db_column='id_exercise_fk')

	# objects=pilatesManager()

	def __str__(self):
		return str("Plan: " + self.name)

	"""
	def __str__(self):
		return str("Plan: " + self.name + " - Dias: " + str(self.total_days)+ " - Id asociado:" + str(self.id_exercise_fk))
	"""
	def save(self, *args, **kwargs):
		self.name = self.name.upper()
		super(Plan, self).save(*args, **kwargs)
