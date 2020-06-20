from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render
from django.views.generic.list import ListView
from .models import Exercise
from apps.exercise_det.models import Exercise_det
from django.views import View
from .forms import CreateExerciseForm, UpdateExerciseForm
from django.shortcuts import render, redirect
from django.http import  HttpResponse

# Create your views here.
class ListExerciseView(ListView):
	model = Exercise
	template_name = 'exercise/list_exercise.html'
	paginate_by = 5

	def get_queryset(self):
		queryset = Exercise.objects.all().order_by("name")
		return queryset

	def get_context_data(self, **kwargs):
		context = super(ListExerciseView, self).get_context_data(**kwargs)
		exercises = self.get_queryset()
		page = self.request.GET.get('page')
		paginator = Paginator(exercises, self.paginate_by)

		try:
			exercises = paginator.page(page)
		except PageNotAnInteger:
		    exercises = paginator.page(1)
		except EmptyPage:
		    exercises = paginator.page(paginator.num_pages)
		context['exercises'] = exercises

		return context

class CreateExerciseView(View):
	template_name= 'exercise/create_exercise.html'

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
		exercise= Exercise.objects.get(id=self.kwargs['pk'])
		form = UpdateExerciseForm(instance=exercise, initial={'primarykey': exercise.pk})

		context={
					'form':form
				}
		return render(request,'exercise/update_exercise.html', context)

class DeleteExerciseView(View):
	def get(self, request, *args, **kwargs):
		exercise = Exercise.objects.get(pk=self.kwargs['pk'])
		exercise.delete()
		return redirect('exercise:list_exercise')


class See(View):
	def get(self, request, *args, **kwargs):
		exercise = Exercise.objects.get(pk=self.kwargs['pk'])
		return render(request, "exercise/see_exercise.html", {"exercise":exercise})
