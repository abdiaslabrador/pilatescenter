from django.db import models
from apps.exercise.models import Exercise


class pilatesManager(models.Manager):
	def pilates(self):
		return Plan.objects.filter(id_exercise_fk__name__iexact='pilates')
	def yoga(self):
		return Plan.objects.filter(id_exercise_fk__name__iexact='yoga')

	def hot_pilates(self):
		return Plan.objects.filter(id_exercise_fk__name__iexact='hot pilates')

# Create your models here.
class Plan(models.Model):
	name 			= models.CharField(null=False, blank=False, max_length=64)
	total_days		= models.IntegerField(null=False, blank=False, default=0)
	oportunities	= models.IntegerField(null=False, blank=False, default=0)

	id_exercise_fk = models.ForeignKey(Exercise, null=True, blank=False, on_delete=models.CASCADE, db_column='id_exercise_fk')

	objects=pilatesManager()

	def __str__(self):
		return str("Plan: " + self.name + " - Dias: " + str(self.total_days)+ " - Id asociado:" + str(self.id_exercise_fk))
