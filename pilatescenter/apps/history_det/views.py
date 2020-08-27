#shortcuts
from django.shortcuts import render, redirect

#models
from apps.exercise.models import Exercise
from apps.create_user.models import CustomUser
from apps.lesson_det.models import Lesson_det


#views
from django.views import View
from django.contrib import messages

#forms
from apps.lesson_det.forms import SearchClassesForm


#------------------------------------------------------------------------------------------
#the general history
#------------------------------------------------------------------------------------------
class ListLessonExerciseHistoryView(View):
	"""Este se muestra los ejercicios """
	template_name= 'history/list_lesson_exercise_history.html'
	context = {}

	def get(self, request, *args, **kwargs):
		#validacion de que sea un superusuario
		if not request.user.is_superuser:
			return redirect('admin_login:login_admin')

		exercises = Exercise.objects.all().order_by('name')	
		context = {
						'exercises':exercises
				  }
		return render(request, self.template_name, context)

class ListHistoryView(View):
	"""Muestra todos los historiales de un ejercicio en la opcion barra-historial""" 
	template_name= 'history/list_history.html'
	context = {}

	def post(self, request, *args, **kwargs):
		form =  SearchClassesForm(request.POST)

		if form.is_valid():
			exercise=Exercise.objects.get(id = self.kwargs['id_exercise'])
			lessons = Lesson_det.objects.filter(
												    id_exercise_fk=exercise,
												    day_lesson__range=(form.cleaned_data['since'],form.cleaned_data['until'])
												    
												).order_by("day_lesson", "hour_lesson")	
			context = {	
						'form':form,
						'exercise':exercise,
						'lessons':lessons,
				       }
			# return HttpResponse("<h1>Todo ok</h1>")
			return render(request, self.template_name, context)
		else:
			print(form.errors.as_data)
			print("something happened")
			exercise=Exercise.objects.get(id = self.kwargs['id_exercise'])
			histories = Lesson_det.objects.filter(id_exercise_fk=exercise).order_by("day_lesson", "hour_lesson")
			context = {		
							'form':form,
							'exercise':exercise,
							'histories':histories,
					  }

		return render(request, self.template_name, context)

	def get(self, request, *args, **kwargs):
		#validacion de que sea un superusuario
		if not request.user.is_superuser:
			return redirect('admin_login:login_admin')

		form = SearchClassesForm()
		exercise=Exercise.objects.get(id = self.kwargs['id_exercise'])
		histories = Lesson_det.objects.filter(
												lesson_status = Lesson_det.FINISHED,
											  	id_exercise_fk=exercise
											  ).order_by("day_lesson", "hour_lesson")
		context = {		
						'form':form,
						'exercise':exercise,
						'histories':histories,
				  }

		return render(request, self.template_name, context)

class GeneralSeeHistoryView(View):
	"""
		this function is to see  all histories (no in the modification user)
	"""
	def get(self, request, *args, **kwargs):
		#validacion de que sea un superusuario
		if not request.user.is_superuser:
			return redirect('admin_login:login_admin')

		try:
			history_det = Lesson_det.objects.get(pk=self.kwargs['id_history'])
		except Lesson.DoesNotExist:
			messages.success(request, 'Este historial que desea manipular fue eliminado o no existe', extra_tags='alert-danger')
			return redirect('history:list_history', id_exercise=self.kwargs['id_exercise'])

		users = CustomUser.objects.filter(lesson_det__id = history_det.id)

		context = {
						'history_det': history_det,
						'users': users,
				   }
		return render(request,'history/history.html', context)


class GeneralDeleteHistoryView(View):
	"""
		this function is to deletes a particular history in the histories (no in the modification user)
	"""
	def get(self, request, *args, **kwargs):
		#validacion de que sea un superusuario
		if not request.user.is_superuser:
			return redirect('admin_login:login_admin')

		try:
			history_det = Lesson_det.objects.get(pk=self.kwargs['id_history'])
		except Lesson_det.DoesNotExist:
			messages.success(request, 'Este historial que desea manipular fue eliminado o no existe', extra_tags='alert-danger')
			return redirect('history:list_history', id_exercise=self.kwargs['id_exercise'])

		history_det.delete()

		return redirect('history:list_history', id_exercise=self.kwargs['id_exercise'])

#------------------------------------------------------------------------------------------
#the user configuration history
#------------------------------------------------------------------------------------------
class UserConfigurationSeeHistoryView(View):
	"""
		here i see a particular history when the button "see" is pressed in the user configuration
	"""
	def get(self, request, *args, **kwargs):
		#validacion de que sea un superusuario
		if not request.user.is_superuser:
			return redirect('admin_login:login_admin')

		try:
			history_det = Lesson_det.objects.get(pk=self.kwargs['id_history'])
		except Lesson_det.DoesNotExist:
			messages.success(request, 'Este historial que desea manipular fue eliminado o no existe', extra_tags='alert-danger')
			return redirect('content_user:user_configuration_history', pk=self.kwargs['id_exercise_det'])

		users = CustomUser.objects.filter(lesson_det__id = history_det.id)

		context = {
						'history_det': history_det,
						'users': users,
				   }
		return render(request,'history/history.html', context)


class UserConfigurationDeleteHistoryView(View):
	"""
		here i delete a particular history when the button "delete" is pressed in the user configuration
	"""
	def get(self, request, *args, **kwargs):
		#validacion de que sea un superusuario
		if not request.user.is_superuser:
			return redirect('admin_login:login_admin')
			
		try:
			history_det = Lesson_det.objects.get(pk=self.kwargs['id_history'])
		except History_det.DoesNotExist:
			messages.success(request, 'Este historial que desea manipular fue eliminado o no existe', extra_tags='alert-danger')
			return redirect('content_user:user_configuration_history', pk=self.kwargs['id_exercise_det'])

		history_det.delete()

		return redirect('content_user:user_configuration_history', pk=self.kwargs['id_exercise_det'])