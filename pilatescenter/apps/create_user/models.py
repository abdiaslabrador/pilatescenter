#These imports are to CustomUser models
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.contrib.auth.password_validation  import validate_password
from .validators  import name_space

#these import are to get a token for each user just have been created
from rest_framework.views import APIView
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


class UserManager(BaseUserManager):
	#Change the password for any user
	def change_password(self, username, password):

		if not username:
			raise ValueError('Los usuarios tienen que tener username')
		if not password:
			raise ValueError('Los usuarios tienen que tener contraseña')

		try:
			user = self.model.objects.get(username=username)
		except self.model.DoesNotExist:
			raise ValueError('username no encontrado')

		try:
			validate_password(password)
		except:
			raise ValueError('La contraseña cumple con los requerimientos')
		user.set_password(password)

		user.save(using=self._db)
		return user

	def create_user(self, username, first_name, last_name, ci, email, password=None):

		if not username:
			raise ValueError('Los usuarios tienen que tener username')
		if not password:
			raise ValueError('Los usuarios tienen que tener contraseña')
		if not first_name:
			raise ValueError('Los usuarios tienen que tener primer nombre')


		user = self.model(  username=username,
							first_name=first_name,
							last_name=last_name,
							ci=ci,
							email=email,
						  )
		user.set_password(password)
		user.save(using=self._db)

		return user


	def create_superuser(self, username, first_name, last_name, ci, email, password):

		user =self.create_user(username,
							    password=password,
							    first_name=first_name,
							    last_name=last_name,
							    ci=ci,
							    email=email,
							   )
		user.is_staff=True
		user.is_superuser=True
		user.save(using=self._db)
		return user

class CustomUser(AbstractBaseUser, PermissionsMixin):
	username		= models.CharField(null=False, blank=False, max_length=28, unique=True, validators=[name_space])
	first_name		= models.CharField(null=False, blank=False, max_length=20)
	last_name		= models.CharField(null=False, blank=False, max_length=20)
	ci 				= models.CharField(null=True, blank=False, max_length=9)
	phone_number	= models.CharField(null=True, blank=False, max_length=11)
	email 			= models.EmailField(null=False, blank=False, max_length=255,unique=True)

	is_active		= models.BooleanField(default=True)
	is_staff		= models.BooleanField(default=False)
	is_visible		= models.BooleanField(default=True)

	date_joined		= models.DateTimeField(default=timezone.now)

	EMAIL_FIELD		= 'email'
	USERNAME_FIELD	= 'username'
	REQUIRED_FIELDS = ['first_name', 'last_name', 'ci','email']

	objects = UserManager()

	def save(self, *args, **kwargs):
		self.username = self.username.lower()
		super(CustomUser, self).save(*args, **kwargs)

	#this two funtions below are inherited from AbstractBaseUser--
	def get_full_name(self):
		return str(self.first_name + " " + self.first_name)

	def get_short_name(self):
		return self.first_name

	def __str__(self):
		return self.username

	def has_module_perms(self, app_label):
		return True

	def has_perm(self, perm, obj=None):
		return True



@receiver(post_save, sender=CustomUser)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

"""class Exercise_det(models.Model):
	name  =	models.CharField(max_length=64)

	total_days	 = models.IntegerField(default=0)
	oportunities = models.IntegerField(default=0)

	enable_lessons 		= models.IntegerField(default=0)
	scheduled_lessons 	= models.IntegerField(default=0)
	saw_lessons = models.IntegerField(default=0)
	bag 		= models.IntegerField(default=0)

	id_plan_fk 	   = models.ForeignKey(Plan, null=True, blank=True, on_delete=models.CASCADE, db_column='id_plan_fk')
	id_exercise_fk = models.ForeignKey(Exercise, null=True, blank=True, on_delete=models.CASCADE, db_column='id_exercise_fk')
	id_user_fk 	   = models.ForeignKey(CustomUser, null=True, blank=True, on_delete=models.CASCADE, db_column='id_customuser_fk')

	def __str__(self):
		return "name: " + str(self.id_user_fk) + " - " + "ejericicio: "+ str(self.id_exercise_fk)"""
