from django.shortcuts import render, redirect
from .models import History_det
from apps.exercise.models import Exercise
from apps.create_user.models import CustomUser
from django.views import View
from .forms import SearchClasses

# Create your views here.
class ListLessonExerciseHistoryView(View):
	template_name= 'history/list_lesson_exercise_history.html'
	context = {}

	def get(self, request, *args, **kwargs):
		exercises = Exercise.objects.all()
		context = {
						'exercises':exercises
				  }
		return render(request, self.template_name, context)

class ListHistoryView(View):
	template_name= 'history/list_history.html'
	context = {}

	def post(self, request, *args, **kwargs):
		form =  SearchClasses(request.POST)

		if form.is_valid():
			exercise=Exercise.objects.get(id = self.kwargs['pk'])
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
		exercise=Exercise.objects.get(id = self.kwargs['pk'])
		histories = History_det.objects.filter(id_exercise_fk=exercise).order_by("day_lesson")	
		context = {		
						'exercise':exercise,
						'histories':histories,
						'form':form
				  }

		return render(request, self.template_name, context)

class SeeHistoryView(View):
	
	def get(self, request, *args, **kwargs):
		history_det = History_det.objects.get(pk=self.kwargs['pk'])
		users = CustomUser.objects.filter(history_det__id = history_det.id)

		context = {
						'history_det': history_det,
						'users': users,
				   }
		return render(request,'history/history.html', context)


class DeleteHistoryView(View):
	def get(self, request, *args, **kwargs):

		history = History_det.objects.get(id=self.kwargs['id_history'])

		exercise_id= history.id_exercise_fk.id
		history.delete()

		return redirect('history:list_history', pk=exercise_id)