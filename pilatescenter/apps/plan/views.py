#generals for tests
from django.http import HttpResponse

#spedific for this view
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic.edit import UpdateView
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

#models
from .models import Plan
from apps.exercise_det.models import Exercise_det
from apps.exercise.models import Exercise
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
			return redirect('Plan:list_plan')
		else:
			print(form.errors.as_data)
			print("something happened")
		return render(request, self.template_name, {'form':form})

	def get(self, request, *args, **kwargs):
		# form =  CreatePlanForm(initial={'name': 'Pepe'})
		form =  CreatePlanForm()
		# (form.errors.as_data)
		return render(request, self.template_name, {'form':form})

class ListPlanView(View):
	def get(self, request, *args, **kwargs):
		contexto= {}
		diccionario_planes={}
		exercises = Exercise.objects.all().order_by("name")
		
		if exercises.count() > 0:
			for exercise in exercises:
				diccionario_planes[exercise.name] = Plan.objects.filter(id_exercise_fk__name__iexact=exercise.name).order_by('name')
			context = {	
						'diccionario_planes' : diccionario_planes
			}
		return render(request,'plan/list_plan.html', context)

class UpdatePlanView(View):
	def post(self, request, *args, **kwargs):
		plan= Plan.objects.get(id=self.kwargs['pk'])
		form = UpdatePlanForm(request.POST, instance=plan)
		if form.is_valid():
			form.save()
			# print("ES VALIDO!")
			return redirect('Plan:list_plan')
		# else:
		# 	print("no es válido")

		return render(request,'plan/update_plan.html', {'form':form})

	def get(self, request, *args, **kwargs):
		plan = Plan.objects.get(id=self.kwargs['pk'])
		form = UpdatePlanForm(instance=plan, initial={'primarykey': plan.pk})
		exercise_obj = Exercise.objects.get(plan__pk=self.kwargs['pk'])

		context={
					'name_exercise': exercise_obj.name,
					'form':form
				}
		return render(request,'plan/update_plan.html', context)

class DeletePlanView(View):
	def get(self, request, *args, **kwargs):
		plan = Plan.objects.get(pk=self.kwargs['pk'])
		"""exercise_dets = Exercise_det.objects.filter(id_plan_fk = self.kwargs['pk'])
		not_one_plan  = Plan.objects.get(name__iexact= "ninguno")

		if exercise_dets.count() > 0:
			for exercise_det in exercise_dets:
				exercise_det.id_plan_fk = not_one_plan
				exercise_det.save()"""
		plan.delete()
		return redirect('Plan:list_plan')

class See(View):
	def get(self, request, *args, **kwargs):
		plan = Plan.objects.get(pk=self.kwargs['pk'])
		return render(request, "plan/see_plan.html", {"plan":plan})
