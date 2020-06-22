from django.shortcuts import render, redirect
from django.views import View
from .forms import Create_hour, UpdateHourForm
from .models import Hour
from apps.exercise.models import Exercise
# Create your views here.

class ListHourView(View):
	template_name= 'class/list_hour.html'

	def get(self, request, *args, **kwargs):
		exercise = Exercise.objects.get(id = self.kwargs['pk'])
		hours = Hour.objects.filter(id_exercise_fk = exercise)

		context = {	'exercise':exercise,
					'hours': hours,	
				   }
		return render(request, self.template_name, context)


class CreateHourView(View):
	template_name= 'class/create_hour.html'

	def post(self, request, *args, **kwargs):
		form =  Create_hour(request.POST)
		if form.is_valid():
			form.save()
			this_hour = Hour.objects.latest('id')	
			exercise = Exercise.objects.get(id=form.cleaned_data['primary_key_exercise'])
			this_hour.id_exercise_fk = exercise
			this_hour.save()
			print("all ok")
			return redirect('lesson:list_hour', pk=form.cleaned_data['primary_key_exercise'])
		else:
			#print(form.errors.as_data)
			print("something happened")
		return render(request, self.template_name, {'form':form})

	def get(self, request, *args, **kwargs):
		
		exercise = Exercise.objects.get(id = self.kwargs['pk'])
		form =  Create_hour(initial={'primary_key_exercise': exercise.id})

		context = {	
					'form':form,
				   }
		# (form.errors.as_data)
		return render(request, self.template_name, context)

class UpdateHourView(View):
	def post(self, request, *args, **kwargs):
		hour = Hour.objects.get(id=self.kwargs['pk'])
		form = UpdateHourForm(request.POST, instance=hour)
		if form.is_valid():
			form.save()
			# print("ES VALIDO!")
			return redirect('lesson:list_hour', pk=hour.id_exercise_fk.id)
		# else:
		# 	print("no es válido")

		return render(request,'class/update_hour.html', {'form':form})

	def get(self, request, *args, **kwargs):
		hour = Hour.objects.get(id=self.kwargs['pk'])
		form = UpdateHourForm(instance=hour, initial={'primarykey': hour.pk})

		context={

					'form':form
				}
		return render(request,'class/update_hour.html', context)


class DeleteHourView(View):
	def get(self, request, *args, **kwargs):
		hour = Hour.objects.get(id=self.kwargs['pk'])
		id_exercise_fk = hour.id_exercise_fk.id
		hour.delete()

		return redirect('lesson:list_hour', pk=id_exercise_fk)	