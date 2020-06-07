from django.db import models
from apps.plan.models import Plan
from apps.exercise.models import Exercise
from apps.create_user.models import CustomUser
from django.db.models import signals



class Exercise_det(models.Model):
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
		return "name: " + str(self.id_user_fk) + " - " + "ejericicio: "+ str(self.id_exercise_fk)


""" 	Esto hace que al eliminar un plan no elimine el Exercise_det asociado,
	lo coloca en null. Esto lo hago con la finalidad de al eliminar un plan no elimine el Exercise_det."""
def set_null(sender, instance, *args, **kwargs):
    """ Aquì se le asigna null a la variable id_plan_fk despuès de ser eliminado"""
    exercise_dets = Exercise_det.objects.filter(id_plan_fk = instance.id)
    not_one_plan  = Plan.objects.get(name__iexact= "ninguno")

    if exercise_dets.count() > 0:
        for exercise_det in exercise_dets:
            exercise_det.id_plan_fk = not_one_plan
            exercise_det.save()

signals.pre_delete.connect(set_null, sender=Plan)
