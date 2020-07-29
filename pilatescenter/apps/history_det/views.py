from django.shortcuts import render, redirect
from .models import History_det
from apps.exercise.models import Exercise
from apps.create_user.models import CustomUser
from django.views import View
from .forms import SearchClasses
from django.contrib import messages

#------------------------------------------------------------------------------------------
#the general history
#------------------------------------------------------------------------------------------
class ListLessonExerciseHistoryView(View):
	"""Este se muestra en la opcion barra-historial"""
	template_name= 'history/list_lesson_exercise_history.html'
	context = {}

	def get(self, request, *args, **kwargs):
		exercises = Exercise.objects.all().order_by('name')	
		context = {
						'exercises':exercises
				  }
		return render(request, self.template_name, context)

class ListHistoryView(View):
	"""Este se muestra en la opcion barra-historial-ejercicio seleccionado"""
	template_name= 'history/list_history.html'
	context = {}

	def post(self, request, *args, **kwargs):
		form =  SearchClasses(request.POST)

		if form.is_valid():
			exercise=Exercise.objects.get(id = self.kwargs['id_exercise'])
			lessons = History_det.objects.filter(
												    id_exercise_fk=exercise,
												    day_lesson__range=(form.cleaned_data['since'],form.cleaned_data['until'])
												    
												).order_by("day_lesson")	
			context = {
						'exercise':exercise,
						'lessons':lessons,
						'form':form
				       }
			# return HttpResponse("<h1>Todo ok</h1>")
			return render(request, self.template_name, context)
		else:
			print(form.errors.as_data)
			print("something happened")
		return render(request, self.template_name, {'form':form})

	def get(self, request, *args, **kwargs):
		form = SearchClasses()
		exercise=Exercise.objects.get(id = self.kwargs['id_exercise'])
		histories = History_det.objects.filter(id_exercise_fk=exercise).order_by("day_lesson")	
		context = {		
						'exercise':exercise,
						'histories':histories,
						'form':form
				  }

		return render(request, self.template_name, context)

class GeneralSeeHistoryView(View):
	def get(self, request, *args, **kwargs):
		try:
			history_det = History_det.objects.get(pk=self.kwargs['id_history'])
		except History_det.DoesNotExist:
			messages.success(request, 'Este historial que desea manipular fue eliminado o no existe', extra_tags='alert-danger')
			return redirect('history:list_history', id_exercise=self.kwargs['id_exercise'])

		users = CustomUser.objects.filter(history_det__id = history_det.id)

		context = {
						'history_det': history_det,
						'users': users,
				   }
		return render(request,'history/history.html', context)


class GeneralDeleteHistoryView(View):
	def get(self, request, *args, **kwargs):

		try:
			history_det = History_det.objects.get(pk=self.kwargs['id_history'])
		except History_det.DoesNotExist:
			messages.success(request, 'Este historial que desea manipular fue eliminado o no existe', extra_tags='alert-danger')
			return redirect('history:list_history', id_exercise=self.kwargs['id_exercise'])

		history_det.delete()

		return redirect('history:list_history', id_exercise=self.kwargs['id_exercise'])

#------------------------------------------------------------------------------------------
#the user configuration history
#------------------------------------------------------------------------------------------
class UserConfigurationSeeHistoryView(View):
	def get(self, request, *args, **kwargs):
		try:
			history_det = History_det.objects.get(pk=self.kwargs['id_history'])
		except History_det.DoesNotExist:
			messages.success(request, 'Este historial que desea manipular fue eliminado o no existe', extra_tags='alert-danger')
			return redirect('content_user:user_configuration_history', pk=self.kwargs['id_exercise_det'])

		users = CustomUser.objects.filter(history_det__id = history_det.id)

		context = {
						'history_det': history_det,
						'users': users,
				   }
		return render(request,'history/history.html', context)


class UserConfigurationDeleteHistoryView(View):
	def get(self, request, *args, **kwargs):

		try:
			history_det = History_det.objects.get(pk=self.kwargs['id_history'])
		except History_det.DoesNotExist:
			messages.success(request, 'Este historial que desea manipular fue eliminado o no existe', extra_tags='alert-danger')
			return redirect('content_user:user_configuration_history', pk=self.kwargs['id_exercise_det'])

		history_det.delete()

		return redirect('content_user:user_configuration_history', pk=self.kwargs['id_exercise_det'])