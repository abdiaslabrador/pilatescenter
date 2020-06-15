from django.db import models

class Exercise(models.Model):
	name  	     = models.CharField(max_length=64)
	description  = models.TextField(null=True, blank=True)
	is_active    = models.BooleanField(default=False)
	def __str__(self):
		return self.name

	def save(self, *args, **kwargs):
		self.name = self.name.upper()
		super(Exercise, self).save(*args, **kwargs)
