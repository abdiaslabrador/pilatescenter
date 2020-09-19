#generals for tests
from django.http import HttpResponse

#spedific for this view
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic.edit import UpdateView
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib import messages
#models
from .models import Plan
from apps.exercise_det.models import Exercise_det
from apps.exercise.models import Exercise
from apps.create_user.models import CustomUser

#forms that will be used
from .forms import CreatePlanForm, UpdatePlanForm



class CreatePlanView(View):
	template_name= 'plan/create_plan.html'

	def post(self, request, *args, **kwargs):
		form =  CreatePlanForm(request.POST)
		if form.is_valid():
			# if (form.cleaned_data['total_days'] % 2) == 0 :
			# 	form.cleaned_data["oportunities"]=int((form.cleaned_data['total_days']/2)-1)
			#   print(form.cleaned_data)
			# print(form.is_bound)
			form.save()
			return redirect('Plan:list_plan', id_exercise= + self.kwargs["id_exercise"])
		else:
			print(form.errors.as_data)
			print("something happened")
		return render(request, self.template_name, {'form':form})

	def get(self, request, *args, **kwargs):
		#validacion de que sea un superusuario
		if not request.user.is_superuser:
			return redirect('admin_login:login_admin')

		try:
			exercise = Exercise.objects.get(id =self.kwargs["id_exercise"])
		except Exercise.DoesNotExist:
			messages.success(request, 'El ejercicio fue eliminado o no existe', extra_tags='alert-danger')
			return redirect('exercise:list_exercise')

		form =  CreatePlanForm(initial = { 'id_exercise_fk': exercise})
		# (form.errors.as_data)
		return render(request, self.template_name, {'form':form})


class ListPlanView(View):
	"""
		here i print the list of the plans as normalsly i do. I pass the users because before to delete the plan i throw a 
		warning message showing the users that are in not reset mode and how are using that plan.
		
	"""
	template_name='plan/list_plan.html'
	contexto= {}
	dic_plans_id={}

	def get(self, request, *args, **kwargs):
		#validacion de que sea un superusuario
		if not request.user.is_superuser:
			return redirect('admin_login:login_admin')

		try:
			exercise = Exercise.objects.get(id =self.kwargs["id_exercise"])
		except Exercise.DoesNotExist:
			messages.success(request, 'El ejercicio fue eliminado o no existe', extra_tags='alert-danger')
			return redirect('exercise:list_exercise')

		plans = Plan.objects.filter(id_exercise_fk=exercise).order_by('name')

		for plan in plans:
			self.dic_plans_id[plan.id] = CustomUser.objects.filter(exercise_det__id_plan_fk=plan,  exercise_det__reset=False)

		

		self.context = {
							'exercise': exercise,
							'plans': plans,
							'dic_plans_id': self.dic_plans_id,
					}

		return render(request, self.template_name, self.context)

class UpdatePlanView(View):
	template_name = 'plan/update_plan.html'
	
	def post(self, request, *args, **kwargs):
		try:
			plan = Plan.objects.get(id=self.kwargs['pk'])
		except Plan.DoesNotExist:
			messages.success(request, 'El plan fue eliminado o no existe', extra_tags='alert-danger')
			return redirect('exercise:list_exercise')

		try:
			exercise_obj = Exercise.objects.get(plan__pk=self.kwargs['pk'])
		except Exercise.DoesNotExist:
			messages.success(request, 'El ejercicio fue eliminado o no existe', extra_tags='alert-danger')
			return redirect('exercise:list_exercise')

		form = UpdatePlanForm(request.POST, instance=plan)

		if form.is_valid():
			form.save()
			# print("ES VALIDO!")
			return redirect('Plan:list_plan', id_exercise=plan.id_exercise_fk.id)
		else:
			print("no es válido")
			context={
						'name_exercise': exercise_obj.name,
						'form':form
				}
		return render(request, self.template_name, context)

	def get(self, request, *args, **kwargs):
		#validacion de que sea un superusuario
		if not request.user.is_superuser:
			return redirect('admin_login:login_admin')

		
		try:
			plan = Plan.objects.get(id=self.kwargs['pk'])
		except Plan.DoesNotExist:
			messages.success(request, 'El plan fue eliminado o no existe', extra_tags='alert-danger')
			return redirect('exercise:list_exercise')

		form = UpdatePlanForm(instance=plan, initial={'primarykey': plan.pk})
		

		try:
			exercise_obj = Exercise.objects.get(plan__pk=self.kwargs['pk'])
		except Exercise.DoesNotExist:
			messages.success(request, 'El ejercicio fue eliminado o no existe', extra_tags='alert-danger')
			return redirect('exercise:list_exercise')

		context={
					'name_exercise': exercise_obj.name,
					'form':form
				}
		return render(request, self.template_name, context)

class DeletePlanView(View):
	def get(self, request, *args, **kwargs):
		#validacion de que sea un superusuario
		if not request.user.is_superuser:
			return redirect('admin_login:login_admin')

		try:
			plan = Plan.objects.get(id=self.kwargs['pk'])
		except Plan.DoesNotExist:
			messages.success(request, 'El plan fue eliminado o no existe', extra_tags='alert-danger')
			return redirect('exercise:list_exercise')
			
		exercises_det = Exercise_det.objects.filter(id_plan_fk=plan)

		for exercise_det in exercises_det:
			if exercise_det.scheduled_lessons > 0:	
				messages.success(request, 'No se puede eliminar un plan con usuarios con clases programadas usando este plan.', extra_tags='alert-danger')
				return redirect('Plan:list_plan', id_exercise=plan.id_exercise_fk.id)


		
		plan.delete()

		return redirect('Plan:list_plan', id_exercise=plan.id_exercise_fk.id)



class See(View):
	def get(self, request, *args, **kwargs):
		#validacion de que sea un superusuario
		if not request.user.is_superuser:
			return redirect('admin_login:login_admin')
			
		try:
			plan = Plan.objects.get(id=self.kwargs['pk'])
		except Plan.DoesNotExist:
			messages.success(request, 'El plan fue eliminado o no existe', extra_tags='alert-danger')
			return redirect('exercise:list_exercise')
		return render(request, "plan/see_plan.html", {"plan":plan})

