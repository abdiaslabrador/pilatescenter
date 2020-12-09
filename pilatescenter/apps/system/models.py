from django.db import models

# Create your models here.
class SystemPilates(models.Model):
	delta_day = models.IntegerField(default=4)
	cant_max = models.IntegerField(default=5)


	def __str__(self):
		return str(self.pk) + str(self.id)