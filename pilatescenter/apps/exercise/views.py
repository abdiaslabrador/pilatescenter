#shortcuts
from django.shortcuts import render, redirect
from django.http import  HttpResponse

#views
from django.views.generic.list import ListView
from django.views import View

#forms
from .forms import CreateExerciseForm, UpdateExerciseForm
from .forms import Create_hour, UpdateHourForm, CreateDayForm

#models
from .models import Exercise
from .models import Hour, Day
from apps.exercise_det.models import Exercise_det

# from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


#------------------------------------------------------------------------------------------
#exercise
#------------------------------------------------------------------------------------------

class ListExerciseView(View):
	"""here i show the list of the exercises"""
	template_name= 'exercise/exercise/list_exercise.html'
	context = {}

	def get(self, request, *args, **kwargs):
		#validacion de que sea un superusuario
		if not request.user.is_superuser:
			return redirect('admin_login:login_admin')

		

		exercises = Exercise.objects.all().order_by("name")
		context = {
						'exercises':exercises
				  }
		return render(request, self.template_name, context)

class CreateExerciseView(View):
	template_name= 'exercise/exercise/create_exercise.html'

	def post(self, request, *args, **kwargs):
		form =  CreateExerciseForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('exercise:list_exercise')
		else:
			#print(form.errors.as_data)
			print("something happened")
		return render(request, self.template_name, {'form':form})

	def get(self, request, *args, **kwargs):
		#validacion de que sea un superusuario
		if not request.user.is_superuser:
			return redirect('admin_login:login_admin')

		# form =  CreatePlanForm(initial={'name': 'Pepe'})
		form =  CreateExerciseForm()
		# (form.errors.as_data)
		return render(request, self.template_name, {'form':form})

class UpdateExerciseView(View):
	def post(self, request, *args, **kwargs):
		exercise= Exercise.objects.get(id=self.kwargs['pk'])
		form = UpdateExerciseForm(request.POST, instance=exercise)
		if form.is_valid():
			form.save()
			exercises_det = Exercise_det.objects.filter(id_exercise_fk=exercise)

			if exercises_det.count() > 0:
				for exercise_det in exercises_det:
					exercise_det.name = exercise.name
					exercise_det.save()

			# print("ES VALIDO!")
			return redirect('exercise:list_exercise')
		# else:
		# 	print("no es válido")

		return render(request,'exercise/update_exercise.html', {'form':form})

	def get(self, request, *args, **kwargs):
		#validacion de que sea un superusuario
		if not request.user.is_superuser:
			return redirect('admin_login:login_admin')

		exercise= Exercise.objects.get(id=self.kwargs['pk'])
		form = UpdateExerciseForm(instance=exercise, initial={'primarykey': exercise.pk})

		context={	
					'exercise':exercise,
					'form':form
				}
		return render(request,'exercise/exercise/update_exercise.html', context)

class DeleteExerciseView(View):
	def get(self, request, *args, **kwargs):
		#validacion de que sea un superusuario
		if not request.user.is_superuser:
			return redirect('admin_login:login_admin')

		exercise = Exercise.objects.get(pk=self.kwargs['pk'])
		exercise.delete()
		return redirect('exercise:list_exercise')


class See(View):
	"""here i see the exercise"""
	def get(self, request, *args, **kwargs):
		#validacion de que sea un superusuario
		if not request.user.is_superuser:
			return redirect('admin_login:login_admin')

		exercise = Exercise.objects.get(pk=self.kwargs['pk'])
		return render(request, "exercise/exercise/see_exercise.html", {"exercise":exercise})



#------------------------------------------------------------------------------------------
#day
#------------------------------------------------------------------------------------------
class ListDayView(View):
	template_name= 'exercise/day/list_day.html'

	def get(self, request, *args, **kwargs):
		#validacion de que sea un superusuario
		if not request.user.is_superuser:
			return redirect('admin_login:login_admin')

		exercise = Exercise.objects.get(id = self.kwargs['pk'])
		days = Day.objects.filter(hour__id_exercise_fk=self.kwargs['pk']).distinct('name').order_by('name')
		context = {	
					'days':days,
					'exercise':exercise,

				   }
		return render(request, self.template_name, context)

class CreateDayView(View):
	template_name= 'exercise/day/create_day.html'

	
	def post(self, request, *args, **kwargs):

		form =  CreateDayForm(request.POST)

		if form.is_valid():
			form.save()
			#after of set the hour, i set the relationship ( exercise )
			exercise = Exercise.objects.get(id = self.kwargs['pk'])
			hour_obj = Hour.objects.latest('id')	
			hour_obj.id_exercise_fk = exercise
			hour_obj.save()
			# return HttpResponse("<h1>Todo ok</h1>")
			return redirect('exercise:list_day', pk=self.kwargs['pk'])
		else:
			#print(form.errors.as_data)
			print("something happened")
		return render(request, self.template_name, {'form':form})

	def get(self, request, *args, **kwargs):
		#validacion de que sea un superusuario
		if not request.user.is_superuser:
			return redirect('admin_login:login_admin')

		form = CreateDayForm()
					
		return render(request, self.template_name, {'form':form})

class DeleteDayView(View):

	def get(self, request, *args, **kwargs):
		#validacion de que sea un superusuario
		if not request.user.is_superuser:
			return redirect('admin_login:login_admin')

		# day = Day.objects.get(name__iexact = self.kwargs['name_day'])
		all_hours = Hour.objects.filter(id_exercise_fk = self.kwargs['pk'], id_day_fk = self.kwargs['id_day'])
		for hour_day in all_hours:
			hour_day.delete()

		return redirect('exercise:list_day', pk=self.kwargs['pk'])
#------------------------------------------------------------------------------------------
#hour
#------------------------------------------------------------------------------------------
class ListHourView(View):
	template_name= 'exercise/hour/list_hour.html'

	def get(self, request, *args, **kwargs):
		#validacion de que sea un superusuario
		if not request.user.is_superuser:
			return redirect('admin_login:login_admin')

		exercise = Exercise.objects.get(id = self.kwargs['pk'])
		day = Day.objects.get(id = self.kwargs['id_day'])
		hours = Hour.objects.filter(id_exercise_fk = exercise,).filter(id_day_fk=day).order_by('hour_lesson')
		context = {	
					'exercise':exercise,
					'hours': hours,
					'day':day,
				   }
		# return HttpResponse("holad")	   
		return render(request, self.template_name, context)


class CreateHourView(View):
	template_name= 'exercise/hour/create_hour.html'

	def post(self, request, *args, **kwargs):

		form =  Create_hour(request.POST)

		if form.is_valid():
			form.save()
			#after of set the hour, i set the relationship ( exercise and day)
			exercise = Exercise.objects.get(id = self.kwargs['pk'])
			day = Day.objects.get(id = self.kwargs['id_day'])
			hour_obj = Hour.objects.latest('id')	
			hour_obj.id_exercise_fk = exercise
			hour_obj.id_day_fk = day
			hour_obj.save()
			# return HttpResponse("<h1>Todo ok</h1>")
			return redirect('exercise:list_hour', pk=self.kwargs['pk'], id_day = self.kwargs['id_day'])
		else:
			#print(form.errors.as_data)
			print("something happened")
		return render(request, self.template_name, {'form':form})

	def get(self, request, *args, **kwargs):
		#validacion de que sea un superusuario
		if not request.user.is_superuser:
			return redirect('admin_login:login_admin')

		form =  Create_hour()
		context = {	
					'form':form,
				  }
		return render(request, self.template_name, context)

class UpdateHourView(View):
	def post(self, request, *args, **kwargs):
		hour = Hour.objects.get(id=self.kwargs['pk'])
		form = UpdateHourForm(request.POST, instance=hour)
		if form.is_valid():
			form.save()
			# print("ES VALIDO!")
			return redirect('exercise:list_hour', pk=hour.id_exercise_fk.id, id_day=self.kwargs['id_day'])
		# else:
		# 	print("no es válido")

		return render(request,'exercise/hour/update_hour.html', {'form':form})

	def get(self, request, *args, **kwargs):
		#validacion de que sea un superusuario
		if not request.user.is_superuser:
			return redirect('admin_login:login_admin')

		hour = Hour.objects.get(id=self.kwargs['pk'])
		form = UpdateHourForm(instance=hour, initial={'primarykey': hour.pk})

		context={

					'form':form
				}
		return render(request,'exercise/hour/update_hour.html', context)


class DeleteHourView(View):
	def get(self, request, *args, **kwargs):
		#validacion de que sea un superusuario
		if not request.user.is_superuser:
			return redirect('admin_login:login_admin')

		hour = Hour.objects.get(id=self.kwargs['pk'])
		id_exercise_fk = hour.id_exercise_fk.id
		hour.delete()

		return redirect('exercise:list_day', pk=id_exercise_fk)	

