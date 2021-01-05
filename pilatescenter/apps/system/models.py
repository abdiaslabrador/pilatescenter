from django.db import models

# Create your models here.
class SystemPilates(models.Model):
	delta_day = models.IntegerField(default=4)
	cant_max = models.IntegerField(default=5)
	reglas = models.TextField( null=True, blank = True)
	

class Contact(models.Model):
	email = models.EmailField( null=False, blank=False, max_length=255, unique=True)
	direction = models.TextField(verbose_name='Dirección', null=True, blank = True)
	phone_number = models.CharField(verbose_name='Número telefónico', null=True, blank=False, max_length=40)
	

	# def __str__(self):
	# 	return str(self.pk) + str(self.id)