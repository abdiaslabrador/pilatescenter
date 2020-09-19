from django.db import models
from apps.plan.models import Plan
from apps.exercise.models import Exercise, Day
from apps.lesson_det.models import Lesson_det
from apps.create_user.models import CustomUser
from apps.devolution.models import Devolution
from django.db.models import signals


class Exercise_det(models.Model):
	name  =	models.CharField(max_length=64)
	devolutions = models.IntegerField(default=0)
	total_days	 = models.IntegerField(default=0)

	enable_lessons 		= models.IntegerField(default=0)
	saw_lessons = models.IntegerField(default=0)
	bag 		= models.IntegerField(default=0)

	scheduled_lessons 	= models.IntegerField(default=0)
	oportunities = models.IntegerField(default=0)

	reset = models.BooleanField(default=True)

	id_plan_fk 	   = models.ForeignKey(Plan,  on_delete=models.CASCADE, db_column='id_plan_fk')
	id_exercise_fk = models.ForeignKey(Exercise, null=True, blank=True, on_delete=models.CASCADE, db_column='id_exercise_fk')
	id_user_fk 	   = models.ForeignKey(CustomUser, null=True, blank=True, on_delete=models.CASCADE, db_column='id_customuser_fk')

	def __str__(self):
		return "name: " + str(self.id_user_fk) + " - " + "ejericicio: "+ str(self.id_exercise_fk)

	def resetter(self):
		"""

		"""
		self.devolutions = Devolution.objects.filter(	
														
														returned = False,
														id_user_fk=self.id_user_fk.id,
														id_lesson_fk = None,
														id_exercise_fk= self.id_exercise_fk,
													).count()

		
		if self.reset == True:
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
		else:

			self.total_days = self.enable_lessons + self.bag
			not_one_plan= None

			try:
				not_one_plan = Plan.objects.get(name__iexact= "ninguno")
			except Plan.DoesNotExist:
				not_one_plan = Plan.objects.create(name= "ninguno")

			self.id_plan_fk = not_one_plan

			self.enable_lessons = self.total_days

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
#devolution signals 
#------------------------------------------------------------------------------------------
def update_devolution_m2m_post_add(sender, instance, action="post_add", *args, **kwargs):
	"""Después de que añado un usuario a una clase, actualizo su resumen"""
	if action == "post_add":

		id_lesson_fk=list(kwargs["pk_set"])
		lesson = Lesson_det.objects.get(id = id_lesson_fk[0])
		
		#actualización del resumen de la lección
		cant_users_devolution = CustomUser.objects.filter(	
															devolution__id_lesson_fk__id=lesson.id
														 ).count()
		
		lesson.cant_in = lesson.id_user_fk.count() + cant_users_devolution
		lesson.quota = lesson.cant_max - lesson.cant_in


		if lesson.cant_in < lesson.cant_max:
			lesson.lesson_capacity_status = Lesson_det.OPEN
			lesson.save()
		elif lesson.cant_in == lesson.cant_max:
			lesson.lesson_capacity_status = Lesson_det.CLOSE
			lesson.save()

		user_exercise_det = Exercise_det.objects.get(
												   id_user_fk= instance.id_user_fk,
												   id_exercise_fk= instance.id_exercise_fk
												)
		
		
		user_exercise_det.devolutions = Devolution.objects.filter(
																id_lesson_fk = None,
																returned = False,
																id_user_fk = instance.id_user_fk,
																id_exercise_fk= instance.id_exercise_fk,
												).count()

		user_exercise_det.scheduled_lessons = Lesson_det.objects.filter(reset= False, id_exercise_fk= instance.id_exercise_fk.id, id_user_fk= instance.id_user_fk).exclude( lesson_status = Lesson_det.FINISHED).count()
		user_exercise_det.saw_lessons = Lesson_det.objects.filter(reset= False, id_exercise_fk= instance.id_exercise_fk, id_user_fk= instance.id_user_fk, lesson_status = Lesson_det.FINISHED).count()
		user_exercise_det.enable_lessons = user_exercise_det.total_days - (user_exercise_det.saw_lessons + user_exercise_det.bag  + user_exercise_det.scheduled_lessons)
		user_exercise_det.save()

signals.m2m_changed.connect(update_devolution_m2m_post_add, sender=Devolution.id_lesson_fk.through)


def update_devolution_m2m_post_remove(sender, instance, action="post_remove", *args, **kwargs):
	"""Actualizo el la lección"""
	if action == "post_remove":
		id_lesson_fk=list(kwargs["pk_set"])

		lesson_is_null = False

		try:
			lesson = Lesson_det.objects.get(id = id_lesson_fk[0])
		except Lesson_det.DoesNotExist:
			lesson_is_null = True
		
		if lesson_is_null == False:  
			#actualización del resumen de la lección
			cant_users_devolution = CustomUser.objects.filter(	
																devolution__id_lesson_fk__id=lesson.id
															 ).count()
			
			lesson.cant_in = lesson.id_user_fk.count() + cant_users_devolution
			lesson.quota = lesson.cant_max - lesson.cant_in


			if lesson.cant_in < lesson.cant_max:
				lesson.lesson_capacity_status = Lesson_det.OPEN
				lesson.save()
			elif lesson.cant_in == lesson.cant_max:
				lesson.lesson_capacity_status = Lesson_det.CLOSE
				lesson.save()
			
		user_exercise_det = Exercise_det.objects.get(
												   id_user_fk= instance.id_user_fk,
												   id_exercise_fk= instance.id_exercise_fk
												)
		
		
		user_exercise_det.devolutions = Devolution.objects.filter(
																id_lesson_fk = None,
																returned = False,
																id_user_fk = instance.id_user_fk,
																id_exercise_fk= instance.id_exercise_fk,
												).count()
		
		user_exercise_det.scheduled_lessons = Lesson_det.objects.filter(reset= False, id_exercise_fk= instance.id_exercise_fk.id, id_user_fk= instance.id_user_fk).exclude( lesson_status = Lesson_det.FINISHED).count()
		user_exercise_det.saw_lessons = Lesson_det.objects.filter(reset= False, id_exercise_fk= instance.id_exercise_fk, id_user_fk= instance.id_user_fk, lesson_status = Lesson_det.FINISHED).count()
		user_exercise_det.enable_lessons = user_exercise_det.total_days - (user_exercise_det.saw_lessons + user_exercise_det.bag  + user_exercise_det.scheduled_lessons)
		user_exercise_det.save()

signals.m2m_changed.connect(update_devolution_m2m_post_remove, sender=Devolution.id_lesson_fk.through)


def preDevolutionDelete(sender, instance, *args, **kwargs):
	""" 
		Esto hace que al eliminar un plan no elimine el Exercise_det asociado,
		asignandole el plan ninguno.
	"""
	lesson = instance.id_lesson_fk.all().first()

	if lesson != None:
		cant_users_devolution = CustomUser.objects.filter(	
															devolution__id_lesson_fk__id=lesson.id
														 ).exclude(devolution__id = instance.id).count()
		
		lesson.cant_in = lesson.id_user_fk.count() + cant_users_devolution
		lesson.quota = lesson.cant_max - lesson.cant_in
		lesson.save()

	user_exercise_det = Exercise_det.objects.get(
											   id_user_fk= instance.id_user_fk,
											   id_exercise_fk= instance.id_exercise_fk
											)
		
		
	user_exercise_det.devolutions = Devolution.objects.filter(
															id_lesson_fk = None,
															returned = False,
															id_user_fk = instance.id_user_fk,
															id_exercise_fk= instance.id_exercise_fk,
												).exclude(id = instance.id).count()

	user_exercise_det.scheduled_lessons = Lesson_det.objects.filter(reset= False, id_exercise_fk= instance.id_exercise_fk.id, id_user_fk= instance.id_user_fk).exclude( lesson_status = Lesson_det.FINISHED).count()
	user_exercise_det.saw_lessons = Lesson_det.objects.filter(reset= False, id_exercise_fk= instance.id_exercise_fk, id_user_fk= instance.id_user_fk, lesson_status = Lesson_det.FINISHED).count()
	user_exercise_det.enable_lessons = user_exercise_det.total_days - (user_exercise_det.saw_lessons + user_exercise_det.bag  + user_exercise_det.scheduled_lessons)
	user_exercise_det.save()


signals.pre_delete.connect(preDevolutionDelete, sender=Devolution)

def postDevolutionDelete(sender, instance, *args, **kwargs):
	""" 
		Esto hace que al eliminar un plan no elimine el Exercise_det asociado,
		asignandole el plan ninguno.
	"""
		
	user_exercise_det = Exercise_det.objects.get(
											   id_user_fk= instance.id_user_fk,
											   id_exercise_fk= instance.id_exercise_fk
											)
		
		
	user_exercise_det.devolutions = Devolution.objects.filter(
															id_lesson_fk = None,
															returned = False,
															id_user_fk = instance.id_user_fk,
															id_exercise_fk= instance.id_exercise_fk,
												).count()

	user_exercise_det.scheduled_lessons = Lesson_det.objects.filter(reset= False, id_exercise_fk= instance.id_exercise_fk.id, id_user_fk= instance.id_user_fk).exclude( lesson_status = Lesson_det.FINISHED).count()
	user_exercise_det.saw_lessons = Lesson_det.objects.filter(reset= False, id_exercise_fk= instance.id_exercise_fk, id_user_fk= instance.id_user_fk, lesson_status = Lesson_det.FINISHED).count()
	user_exercise_det.enable_lessons = user_exercise_det.total_days - (user_exercise_det.saw_lessons + user_exercise_det.bag  + user_exercise_det.scheduled_lessons)
	user_exercise_det.save()


signals.post_delete.connect(postDevolutionDelete, sender=Devolution)

def postDevolutionSave(sender, instance, *args, **kwargs):
	""" 
		Esto hace que al eliminar un plan no elimine el Exercise_det asociado,
		asignandole el plan ninguno.
	"""
	lesson = instance.id_lesson_fk.all().first()
	if lesson != None:
		#actualización del resumen de la lección
		cant_users_devolution = CustomUser.objects.filter(	
															devolution__id_lesson_fk__id=lesson.id
														 ).count()
		
		lesson.cant_in = lesson.id_user_fk.count() + cant_users_devolution
		lesson.quota = lesson.cant_max - lesson.cant_in

		

		if lesson.cant_in < lesson.cant_max:
			lesson.lesson_capacity_status = Lesson_det.OPEN
			lesson.save()
		elif lesson.cant_in == lesson.cant_max:
			lesson.lesson_capacity_status = Lesson_det.CLOSE
			lesson.save()
	else:

		user_exercise_det = Exercise_det.objects.get(
												   id_user_fk= instance.id_user_fk,
												   id_exercise_fk= instance.id_exercise_fk
												)
			
			
		user_exercise_det.devolutions = Devolution.objects.filter(
																	id_lesson_fk = None,
																	returned = False,
																	id_user_fk = instance.id_user_fk,
																	id_exercise_fk= instance.id_exercise_fk,
													).count()
			
		user_exercise_det.scheduled_lessons = Lesson_det.objects.filter(reset= False, id_exercise_fk= instance.id_exercise_fk.id, id_user_fk= instance.id_user_fk).exclude( lesson_status = Lesson_det.FINISHED).count()
		user_exercise_det.saw_lessons = Lesson_det.objects.filter(reset= False, id_exercise_fk= instance.id_exercise_fk, id_user_fk= instance.id_user_fk, lesson_status = Lesson_det.FINISHED).count()
		user_exercise_det.enable_lessons = user_exercise_det.total_days - (user_exercise_det.saw_lessons + user_exercise_det.bag  + user_exercise_det.scheduled_lessons)
		user_exercise_det.save()


signals.post_save.connect(postDevolutionSave, sender=Devolution)


#------------------------------------------------------------------------------------------
#lesson signals 
#------------------------------------------------------------------------------------------
def preSaveLesson(sender, instance,  *args, **kwargs):
	if instance.cant_in == 0:
		instance.lesson_capacity_status= instance.NOTONE
	elif instance.cant_in == instance.cant_max:
		instance.lesson_capacity_status = Lesson_det.CLOSE
	elif instance.cant_in > 0 and instance.cant_in < instance.cant_max:
		instance.lesson_capacity_status = Lesson_det.OPEN

signals.pre_save.connect(preSaveLesson, sender=Lesson_det)


def postSaveLesson(sender, instance, created,  *args, **kwargs):

	#Los usuarios de la leccion
	

	users_in_instance = instance.id_user_fk.all()	
	for user in users_in_instance:
		user_exercise_det = Exercise_det.objects.get(id_exercise_fk= instance.id_exercise_fk, id_user_fk= user)

		#Esta el la cantidad de clases programadas del usuario
		user_exercise_det.scheduled_lessons = Lesson_det.objects.filter(
															reset=False,
                                                            id_exercise_fk= instance.id_exercise_fk, 
                                                            id_user_fk= user,
                                                          ).exclude(lesson_status = Lesson_det.FINISHED).count()

		user_exercise_det.devolutions = Devolution.objects.filter(
																	id_lesson_fk = None,
																	returned = False,
																	id_user_fk = user_exercise_det.id_user_fk,
																	id_exercise_fk= instance.id_exercise_fk,
													).count()

		user_exercise_det.saw_lessons = Lesson_det.objects.filter(reset= False, id_exercise_fk= user_exercise_det.id_exercise_fk, id_user_fk= user_exercise_det.id_user_fk, lesson_status = Lesson_det.FINISHED).count()
		user_exercise_det.enable_lessons = user_exercise_det.total_days - (user_exercise_det.saw_lessons + user_exercise_det.bag  + user_exercise_det.scheduled_lessons)
		user_exercise_det.save()	


signals.post_save.connect(postSaveLesson, sender=Lesson_det)


def preDeleteLesson(sender, instance,  *args, **kwargs):

	users_in_lesson = CustomUser.objects.filter(	
													lesson_det__id=instance.id
									 			)
	for user in users_in_lesson:
		instance.id_user_fk.remove(user)

	users_in_devolutions = CustomUser.objects.filter(	
														devolution__id_lesson_fk__id=instance.id
									 				).order_by("username").distinct("username")

	for user in users_in_devolutions:
		exercise_det = Exercise_det.objects.get(
												   id_user_fk= user,
												   id_exercise_fk= instance.id_exercise_fk
												)

		devolution = Devolution.objects.filter(				
													returned = False,
													id_user_fk = user,
													id_lesson_fk = instance.id,
													id_exercise_fk= instance.id_exercise_fk,
												).first()

		devolution.id_lesson_fk.remove(instance)

signals.pre_delete.connect(preDeleteLesson, sender=Lesson_det)

	
def update_lesson_m2m_post_add(sender, instance, action="post_add", *args, **kwargs):
	"""Después de que añado un usuario a una clase, actualizo su resumen"""
	if action == "post_add":
		id_user_fk=list(kwargs["pk_set"])

		for user in id_user_fk:			
			user_exercise_det = Exercise_det.objects.get( id_exercise_fk= instance.id_exercise_fk, id_user_fk= user)
			
			#actualización del resumen del usuario
			user_exercise_det.devolutions = Devolution.objects.filter(
																	id_lesson_fk = None,
																	returned = False,
																	id_user_fk = user_exercise_det.id_user_fk,
																	id_exercise_fk= instance.id_exercise_fk,
													).count()

			user_exercise_det.scheduled_lessons = Lesson_det.objects.filter(reset= False, id_exercise_fk= instance.id_exercise_fk, id_user_fk= user).exclude(lesson_status = Lesson_det.FINISHED).count()
			user_exercise_det.saw_lessons = Lesson_det.objects.filter(reset= False, id_exercise_fk= instance.id_exercise_fk, id_user_fk= user, lesson_status = Lesson_det.FINISHED).count()
			user_exercise_det.enable_lessons = user_exercise_det.total_days - (user_exercise_det.saw_lessons + user_exercise_det.bag  + user_exercise_det.scheduled_lessons)
			user_exercise_det.save()

		#actualización del resumen de la lección
		users_devolution = CustomUser.objects.filter(	
															devolution__id_lesson_fk__id=instance.id
														 ).count()


		instance.cant_in = instance.id_user_fk.count() + users_devolution
		instance.quota = instance.cant_max - instance.cant_in


		if instance.cant_in < instance.cant_max:
			instance.lesson_capacity_status = Lesson_det.OPEN
			instance.save()
		elif instance.cant_in == instance.cant_max:
			instance.lesson_capacity_status = Lesson_det.CLOSE
			instance.save()
		
signals.m2m_changed.connect(update_lesson_m2m_post_add, sender=Lesson_det.id_user_fk.through)


def update_lesson_m2m_post_remove(sender, instance, action="post_remove", *args, **kwargs):
	"""Actualizo el la lección"""
	if action == "post_remove":
		id_user_fk=list(kwargs["pk_set"])#este es la id del usuario pasado por parametros en el "remove()"

		for user in id_user_fk:			
			user_exercise_det = Exercise_det.objects.get( id_exercise_fk= instance.id_exercise_fk.id, id_user_fk= user)
			#Esta el la cantidad de clases programadas del usuario
			user_exercise_det.devolutions = Devolution.objects.filter(
																		id_lesson_fk = None,
																		returned = False,
																		id_user_fk = user_exercise_det.id_user_fk,
																		id_exercise_fk= instance.id_exercise_fk,
																	).count()

			user_exercise_det.scheduled_lessons = Lesson_det.objects.filter(reset= False, id_exercise_fk= instance.id_exercise_fk.id, id_user_fk= user).exclude( lesson_status = Lesson_det.FINISHED).count()
			user_exercise_det.saw_lessons = Lesson_det.objects.filter(reset= False, id_exercise_fk= instance.id_exercise_fk, id_user_fk= user, lesson_status = Lesson_det.FINISHED).count()
			user_exercise_det.enable_lessons = user_exercise_det.total_days - (user_exercise_det.saw_lessons + user_exercise_det.bag  + user_exercise_det.scheduled_lessons)
			user_exercise_det.save()

		#actualización del resumen de la lección
		cant_users_devolution = CustomUser.objects.filter(	
														
															devolution__id_lesson_fk__id=instance.id
														 ).count()
		
		instance.cant_in = instance.id_user_fk.count() + cant_users_devolution
		instance.quota = instance.cant_max - instance.cant_in


		if instance.cant_in < instance.cant_max:
			instance.lesson_capacity_status = Lesson_det.OPEN
			instance.save()
		elif instance.cant_in == instance.cant_max:
			instance.lesson_capacity_status = Lesson_det.CLOSE
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

		cant_users_devolution = CustomUser.objects.filter(	
															devolution__id_lesson_fk__id=instance.id
														 ).count()
		
		instance.cant_in = instance.id_user_fk.count() + cant_users_devolution
		instance.quota = instance.cant_max - instance.cant_in
		
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
		user_exercise_det.devolutions = Devolution.objects.filter(
																	id_lesson_fk = None,
																	returned = False,
																	id_user_fk = user_exercise_det.id_user_fk,
																	id_exercise_fk= user_exercise_det.id_exercise_fk,
													).count()

		user_exercise_det.scheduled_lessons = Lesson_det.objects.filter(reset= False, id_exercise_fk= lesson.id_exercise_fk, id_user_fk= user).exclude(id=lesson.id).exclude( lesson_status = Lesson_det.FINISHED).count()
		user_exercise_det.saw_lessons = Lesson_det.objects.filter(reset= False, id_exercise_fk= user_exercise_det.id_exercise_fk, id_user_fk= user_exercise_det.id_user_fk, lesson_status = Lesson_det.FINISHED).count()
		user_exercise_det.enable_lessons = user_exercise_det.total_days - (user_exercise_det.saw_lessons + user_exercise_det.bag  + user_exercise_det.scheduled_lessons)
		user_exercise_det.save()