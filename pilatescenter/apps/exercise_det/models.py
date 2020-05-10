from django.db import models
from apps.plan.models import Plan
from apps.exercise.models import Exercise
from apps.create_user.models import CustomUser
# from django.db.models.signals import post_save
	
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


# def post_user_save(sender, instance, *args, **kwargs):

# 	if kwargs['update_fields'] is None:
# 		plan=Plan.objects.get(name__icontains="x")
# 		exercise=Exercise.objects.get(id=1)
# 		x=Exercise_det.objects.create(name=exercise.name, id_plan_fk=plan, id_exercise_fk=exercise, id_user_fk=instance)
# 		x.save()

# 		exercise=Exercise.objects.get(id=2)
# 		y=Exercise_det.objects.create(name=exercise.name, id_plan_fk=plan, id_exercise_fk=exercise, id_user_fk=instance)
# 		y.save()

# 		exercise=Exercise.objects.get(id=3)
# 		z=Exercise_det.objects.create(name=exercise.name, id_plan_fk=plan, id_exercise_fk=exercise, id_user_fk=instance)
# 		z.save()
# 	else:
# 		print("no actualizó")

# post_save.connect(post_user_save, sender=CustomUser) 
	
