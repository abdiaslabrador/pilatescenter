from django.db import models

class Exercise(models.Model):
	name  	     = models.CharField(max_length=64)
	description  = models.TextField(null=True, blank=True)

	def __str__(self):
		return self.name