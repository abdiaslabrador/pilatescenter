from django.db import models
from apps.plan.models import Plan
from apps.exercise.models import Exercise, Day
from apps.lesson_det.models import Lesson_det
from apps.create_user.models import CustomUser
from django.db.models import signals


class Exercise_det(models.Model):
	name  =	models.CharField(max_length=64)

	total_days	 = models.IntegerField(default=0)

	enable_lessons 		= models.IntegerField(default=0)
	saw_lessons = models.IntegerField(default=0)
	bag 		= models.IntegerField(default=0)

	scheduled_lessons 	= models.IntegerField(default=0)
	oportunities = models.IntegerField(default=0)

	reset = models.BooleanField(default=True)

	id_plan_fk 	   = models.ForeignKey(Plan, null=True, blank=True, on_delete=models.CASCADE, db_column='id_plan_fk')
	id_exercise_fk = models.ForeignKey(Exercise, null=True, blank=True, on_delete=models.CASCADE, db_column='id_exercise_fk')
	id_user_fk 	   = models.ForeignKey(CustomUser, null=True, blank=True, on_delete=models.CASCADE, db_column='id_customuser_fk')

	def __str__(self):
		return "name: " + str(self.id_user_fk) + " - " + "ejericicio: "+ str(self.id_exercise_fk)

	def resetter(self):
		"""
			Aquí yo obtengo todas las clases que han sido vista por este usuario,
		 	luego de obtenerlo lo saco de las clases vistas
		"""
		self.total_days = self.id_plan_fk.total_days
		self.enable_lessons = self.id_plan_fk.total_days

		Lesson_det.objects.filter(
									reset= False,
									lesson_status = Lesson_det.FINISHED,
									id_exercise_fk= self.id_exercise_fk,
									id_user_fk= self.id_user_fk
								).update(reset=True)
		self.saw_lessons = 0
							
		self.bag = 0

		self.oportunities = self.id_plan_fk.oportunities
		self.scheduled_lessons = Lesson_det.objects.filter(
																reset= False,
																id_exercise_fk= self.id_exercise_fk,
																id_user_fk= self.id_user_fk
														   ).exclude(lesson_status = Lesson_det.FINISHED).count()
		self.save()

		# si existen clases vistas y sin personas, en esta operación eliminamos esas lecciones
		# saw_lessons = Lesson_det.objects.filter(
		# 											lesson_status = Lesson_det.FINISHED,
		# 											id_exercise_fk= self.id_exercise_fk
		# 										)
		# for saw_lesson in saw_lessons:
		# 	if saw_lesson.id_user_fk.all().count() == 0:
		# 		saw_lesson.delete()




def set_plan_ninguno_after_exercise_det_deleted(sender, instance, *args, **kwargs):
    """ 
		Esto hace que al eliminar un plan no elimine el Exercise_det asociado,
		asignandole el plan ninguno.
	"""
    exercise_dets = Exercise_det.objects.filter(id_plan_fk = instance)

    not_one_plan= None
    try:
        not_one_plan = Plan.objects.get(name__iexact= "ninguno")
    except Plan.DoesNotExist:
        not_one_plan = Plan.objects.create(name= "ninguno")

    if exercise_dets.count() > 0:
	    for exercise_det in exercise_dets:
	        exercise_det.id_plan_fk = not_one_plan
	        if exercise_det.reset == True:
	            exercise_det.resetter()
	        else:
	            exercise_det.save()
signals.pre_delete.connect(set_plan_ninguno_after_exercise_det_deleted, sender=Plan)


def asign_exercise_det(sender, instance, created, *args, **kwargs):
	"""
 		Este signal asigna el ejercicio que se acaba de crear a todos los usuarios
	"""
	if created:
		users=CustomUser.objects.all()

		not_one_plan= None

		try:
			not_one_plan = Plan.objects.get(name__iexact= "ninguno")
		except Plan.DoesNotExist:
			not_one_plan = Plan.objects.create(name= "ninguno")

		for user in users:
			Exercise_det.objects.create(name=instance.name, id_plan_fk=not_one_plan, id_exercise_fk=instance, id_user_fk=user)
signals.post_save.connect(asign_exercise_det, sender=Exercise)



def asign_exercise_after_user_created(sender, instance, created, *args, **kwargs):
	"""
 		Este signal asigna todos los ejercicios que existen con el plan ninguno a un usuario cuando es creado.
 		Aparte de esto crea los dìas de la semana por si no están creados
	"""
	if created:
		exercises=Exercise.objects.all()
		not_one_plan= None

		if not Day.objects.all():
			Day.objects.create(name="lunes")
			Day.objects.create(name="martes")
			Day.objects.create(name="miercoles")
			Day.objects.create(name="jueves")
			Day.objects.create(name="viernes")
			Day.objects.create(name="sabado")
			Day.objects.create(name="domingo")

		if exercises.count() > 0:
			try:
				not_one_plan = Plan.objects.get(name__iexact= "ninguno")
			except Plan.DoesNotExist:
				not_one_plan = Plan.objects.create(name= "ninguno")

			for i in exercises:
				Exercise_det.objects.create(
												name=i.name,
												id_plan_fk=not_one_plan,
												id_exercise_fk=i,
												id_user_fk=instance
											)
signals.post_save.connect(asign_exercise_after_user_created, sender=CustomUser)



#------------------------------------------------------------------------------------------
#lesson signals 
#------------------------------------------------------------------------------------------

def postSaveLesson(sender, instance,  *args, **kwargs):
	if instance.cant_in == 0:
		instance.lesson_capacity_status= instance.NOTONE
	elif instance.cant_in == instance.cant_max:
		instance.lesson_capacity_status = Lesson_det.CLOSE
	elif instance.cant_in > 0 and instance.cant_in < instance.cant_max:
		instance.lesson_capacity_status = Lesson_det.OPEN

signals.pre_save.connect(postSaveLesson, sender=Lesson_det)

def update_lesson_m2m_post_add(sender, instance, action="post_add", *args, **kwargs):
	"""Después de que añado un usuario a una clase, actualizo su resumen"""
	if action == "post_add":
		id_user_fk=list(kwargs["pk_set"])
		user_exercise_det = Exercise_det.objects.get( id_exercise_fk= instance.id_exercise_fk, id_user_fk= id_user_fk[0])
		
		# #Esta el la cantidad de clases programadas del usuario
		user_exercise_det.scheduled_lessons = Lesson_det.objects.filter(reset= False, id_exercise_fk= instance.id_exercise_fk, id_user_fk= id_user_fk[0]).exclude(lesson_status = Lesson_det.FINISHED).count()
		user_exercise_det.saw_lessons = Lesson_det.objects.filter(reset= False, id_exercise_fk= instance.id_exercise_fk, id_user_fk= id_user_fk[0], lesson_status = Lesson_det.FINISHED).count()
		user_exercise_det.enable_lessons = user_exercise_det.total_days - (user_exercise_det.saw_lessons + user_exercise_det.bag  + user_exercise_det.scheduled_lessons)
		user_exercise_det.save()

		instance.custom_update_lesson()
		if instance.cant_in < instance.cant_max:
			instance.lesson_capacity_status = Lesson_det.OPEN
			instance.save()
		elif instance.cant_in == instance.cant_max:
			instance.lesson_capacity_status = Lesson_det.CLOSE
			instance.save()

signals.m2m_changed.connect(update_lesson_m2m_post_add, sender=Lesson_det.id_user_fk.through)


def update_lesson_m2m_pre_remove(sender, instance, action="pre_remove", *args, **kwargs):
	"""Antes de que eliminar un usuario a una clase, actualizo su resumen"""
	if action == "pre_remove":
		id_user_fk=list(kwargs["pk_set"])#este es la id del usuario pasado por parametros en el "remove()"

		user_exercise_det = Exercise_det.objects.get( id_exercise_fk= instance.id_exercise_fk.id, id_user_fk= id_user_fk[0])
		#Esta el la cantidad de clases programadas del usuario
		user_exercise_det.scheduled_lessons = Lesson_det.objects.filter(reset= False, id_exercise_fk= instance.id_exercise_fk.id, id_user_fk= id_user_fk[0]).exclude(id=instance.id).exclude( lesson_status = Lesson_det.FINISHED).count()
		user_exercise_det.saw_lessons = Lesson_det.objects.filter(reset= False, id_exercise_fk= instance.id_exercise_fk, id_user_fk= id_user_fk[0], lesson_status = Lesson_det.FINISHED).count()
		user_exercise_det.enable_lessons = user_exercise_det.total_days - (user_exercise_det.saw_lessons + user_exercise_det.bag  + user_exercise_det.scheduled_lessons)
		user_exercise_det.save()
signals.m2m_changed.connect(update_lesson_m2m_pre_remove, sender=Lesson_det.id_user_fk.through)

def update_lesson_m2m_post_remove(sender, instance, action="post_remove", *args, **kwargs):
	"""Actualizo el la lección"""
	if action == "post_remove":
		instance.custom_update_lesson()
		if instance.cant_in == 0:
			instance.lesson_capacity_status = Lesson_det.NOTONE
			instance.save()
		else:
			instance.lesson_capacity_status = Lesson_det.OPEN
			instance.save()

signals.m2m_changed.connect(update_lesson_m2m_post_remove, sender=Lesson_det.id_user_fk.through)


def update_lesson_m2m_pre_clear(sender, instance, action="pre_clear", *args, **kwargs):
	"""Actualizo el resnumen"""
	if action == "pre_clear":
		update_resumen(instance)
signals.m2m_changed.connect(update_lesson_m2m_pre_clear, sender=Lesson_det.id_user_fk.through)

def update_lesson_m2m_post_clear(sender, instance, action="post_clear", *args, **kwargs):
	"""Actualizo  la lección"""
	if action == "post_clear":
		instance.custom_update_lesson()
		
		instance.lesson_capacity_status = Lesson_det.NOTONE
		instance.save()

signals.m2m_changed.connect(update_lesson_m2m_post_clear, sender=Lesson_det.id_user_fk.through)

#------------------------------------------------------------------------------------------
#funciones
#------------------------------------------------------------------------------------------

#this function updates the "summary" of the exercise related to the lesson
def update_resumen(lesson):
	"""In the for of this function i don't take in count the actual lesson"""

	#Los usuarios de la leccion
	users_in_lesson = lesson.id_user_fk.all()	
	for user in users_in_lesson:
		user_exercise_det = Exercise_det.objects.get(id_exercise_fk= lesson.id_exercise_fk, id_user_fk= user)

		#Esta el la cantidad de clases programadas del usuario
		user_exercise_det.scheduled_lessons = Lesson_det.objects.filter(reset= False, id_exercise_fk= lesson.id_exercise_fk, id_user_fk= user).exclude(id=lesson.id).exclude( lesson_status = Lesson_det.FINISHED).count()
		user_exercise_det.saw_lessons = Lesson_det.objects.filter(reset= False, id_exercise_fk= user_exercise_det.id_exercise_fk, id_user_fk= user_exercise_det.id_user_fk, lesson_status = Lesson_det.FINISHED).count()
		user_exercise_det.enable_lessons = user_exercise_det.total_days - (user_exercise_det.saw_lessons + user_exercise_det.bag  + user_exercise_det.scheduled_lessons)
		user_exercise_det.save()