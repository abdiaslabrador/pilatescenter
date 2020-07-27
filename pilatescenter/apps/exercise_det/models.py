from django.db import models
from apps.plan.models import Plan
from apps.exercise.models import Exercise
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
		#Aquí yo obtengo todas las clases que han sido vista por este usuario, luego de obtenerlo lo saco de las clases vistas
		saw_lessons = Lesson_det.objects.filter(saw= True, id_exercise_fk= self.id_exercise_fk, id_user_fk= self.id_user_fk)
		for saw_lesson in saw_lessons:
			saw_lesson.id_user_fk.remove(self.id_user_fk)

		self.total_days = self.id_plan_fk.total_days

		self.enable_lessons = self.id_plan_fk.total_days
		self.saw_lessons = Lesson_det.objects.filter(saw= True, id_exercise_fk= self.id_exercise_fk, id_user_fk= self.id_user_fk ).count()
		self.bag = 0

		self.oportunities = self.id_plan_fk.oportunities
		self.scheduled_lessons = Lesson_det.objects.filter(saw= False, id_exercise_fk= self.id_exercise_fk, id_user_fk= self.id_user_fk).count()
		self.save()

		saw_lessons = Lesson_det.objects.filter(saw= True, id_exercise_fk= self.id_exercise_fk)
		for saw_lesson in saw_lessons:
			if saw_lesson.id_user_fk.all().count() == 0:
				saw_lesson.delete()



""" 
	Esto hace que al eliminar un plan no elimine el Exercise_det asociado,
	lo coloca en null. Esto lo hago con la finalidad de al eliminar un plan no elimine el Exercise_det.
"""
def set_null(sender, instance, *args, **kwargs):
    """ Aquì se le asigna null a la variable id_plan_fk despuès de ser eliminado"""
    exercise_dets = Exercise_det.objects.filter(id_plan_fk = instance)
    not_one_plan  = Plan.objects.get(name__iexact= "ninguno")

    if exercise_dets.count() > 0:
	    for exercise_det in exercise_dets:
	        exercise_det.id_plan_fk = not_one_plan
	        if exercise_det.reset == True:
	            exercise_det.resetter()
	        else:
	            exercise_det.save()
signals.pre_delete.connect(set_null, sender=Plan)

"""
 	Este signal asigna el ejercicio creado a todos los usuarios
"""
def asign_exercise_det(sender, instance, created, *args, **kwargs):
	if created:
		users=CustomUser.objects.all()
		plan=Plan.objects.get(name__icontains="ninguno")

		for user in users:
			Exercise_det.objects.create(name=instance.name, id_plan_fk=plan, id_exercise_fk=instance, id_user_fk=user)
signals.post_save.connect(asign_exercise_det, sender=Exercise)


"""
	Este signal le asigna todos los ejercicios disponibles a un usuario cuando es creado
"""
def asign_exercise_after_user_created(sender, instance, created, *args, **kwargs):
	if created:
		exercises=Exercise.objects.all()
		if exercises.count() > 0:
			plan=Plan.objects.get(name__iexact="ninguno")

			for i in exercises:
				Exercise_det.objects.create(name=i.name, id_plan_fk=plan, id_exercise_fk=i, id_user_fk=instance)
signals.post_save.connect(asign_exercise_after_user_created, sender=CustomUser)



#------------------------------------------------------------------------------------------
#lesson signals 
#------------------------------------------------------------------------------------------
def update_lesson_m2m_post_add(sender, instance, action="post_add", *args, **kwargs):
	if action == "post_add":
		id_user_fk=list(kwargs["pk_set"])
		user_exercise_det = Exercise_det.objects.get(id_exercise_fk= instance.id_exercise_fk, id_user_fk= id_user_fk[0])
		
		# #Esta el la cantidad de clases programadas del usuario
		user_exercise_det.scheduled_lessons = Lesson_det.objects.filter(id_exercise_fk= instance.id_exercise_fk, id_user_fk= id_user_fk[0], saw= False).count()
		user_exercise_det.saw_lessons = Lesson_det.objects.filter(id_exercise_fk= instance.id_exercise_fk, id_user_fk= id_user_fk[0], saw= True).count()
		user_exercise_det.enable_lessons = user_exercise_det.total_days - (user_exercise_det.saw_lessons + user_exercise_det.bag  + user_exercise_det.scheduled_lessons)
		user_exercise_det.save()

		instance.custom_update_lesson()
signals.m2m_changed.connect(update_lesson_m2m_post_add, sender=Lesson_det.id_user_fk.through)


def update_lesson_m2m_pre_remove(sender, instance, action="pre_remove", *args, **kwargs):
	if action == "pre_remove":
		id_user_fk=list(kwargs["pk_set"])#este es la id del usuario pasado por parametros en el "remove()"

		user_exercise_det = Exercise_det.objects.get(id_exercise_fk= instance.id_exercise_fk.id, id_user_fk= id_user_fk[0])
		#Esta el la cantidad de clases programadas del usuario
		user_exercise_det.scheduled_lessons = Lesson_det.objects.filter(id_exercise_fk= instance.id_exercise_fk.id, id_user_fk= id_user_fk[0], saw= False).exclude(id=instance.id).count()
		user_exercise_det.saw_lessons = Lesson_det.objects.filter(id_exercise_fk= instance.id_exercise_fk, id_user_fk= id_user_fk[0], saw= True).count()
		user_exercise_det.enable_lessons = user_exercise_det.total_days - (user_exercise_det.saw_lessons + user_exercise_det.bag  + user_exercise_det.scheduled_lessons)
		user_exercise_det.save()
signals.m2m_changed.connect(update_lesson_m2m_pre_remove, sender=Lesson_det.id_user_fk.through)

def update_lesson_m2m_post_remove(sender, instance, action="post_remove", *args, **kwargs):
	if action == "post_remove":
		instance.custom_update_lesson()
signals.m2m_changed.connect(update_lesson_m2m_post_remove, sender=Lesson_det.id_user_fk.through)


def update_lesson_m2m_pre_clear(sender, instance, action="pre_clear", *args, **kwargs):
	if action == "pre_clear":
		update_resumen(instance)
signals.m2m_changed.connect(update_lesson_m2m_pre_clear, sender=Lesson_det.id_user_fk.through)

def update_lesson_m2m_post_clear(sender, instance, action="post_clear", *args, **kwargs):
	if action == "post_clear":
		instance.custom_update_lesson()
signals.m2m_changed.connect(update_lesson_m2m_post_clear, sender=Lesson_det.id_user_fk.through)

#------------------------------------------------------------------------------------------
#funciones
#------------------------------------------------------------------------------------------
def update_resumen(lesson):
	#Los usuarios de la leccion
	users_in_lesson = lesson.id_user_fk.all()	
	for user in users_in_lesson:
		user_exercise_det = Exercise_det.objects.get(id_exercise_fk= lesson.id_exercise_fk, id_user_fk= user)

		#Esta el la cantidad de clases programadas del usuario
		user_exercise_det.scheduled_lessons = Lesson_det.objects.filter(id_exercise_fk= lesson.id_exercise_fk, id_user_fk= user, saw= False).exclude(id=lesson.id).count()
		user_exercise_det.saw_lessons = Lesson_det.objects.filter(id_exercise_fk= user_exercise_det.id_exercise_fk, id_user_fk= user_exercise_det.id_user_fk, saw= True).count()
		user_exercise_det.enable_lessons = user_exercise_det.total_days - (user_exercise_det.saw_lessons + user_exercise_det.bag  + user_exercise_det.scheduled_lessons)
		user_exercise_det.save()