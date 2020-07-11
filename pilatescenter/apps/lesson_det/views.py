from django.shortcuts import render, redirect
from django.views import View
from .forms import ( 
					 CreateLessonForm, CreateLessonSearchForm,
				     SearchClasses, UpdateLessonForm 
				    )
from django.http import HttpResponse
from apps.exercise.models import Exercise, Hour
from apps.exercise_det.models import Exercise_det
from apps.history_det.models import History_det
from apps.create_user.models import CustomUser
from .models import Lesson_det
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib import messages
import datetime

#------------------------------------------------------------------------------------------
#lesson
#------------------------------------------------------------------------------------------
class CreateLessonView(View):
	template_name= 'lesson/create_lesson.html'

	def post(self, request, *args, **kwargs):
		form =  CreateLessonForm(request.POST)

		if form.is_valid():
			pk=form.cleaned_data['id_exercise_fk'].id
			year=form.cleaned_data['day_lesson'].year
			month=form.cleaned_data['day_lesson'].month
			day=form.cleaned_data['day_lesson'].day
			# return HttpResponse("<h1>Todo ok</h1>")

			return redirect('lesson:create_lesson_form_search', pk=pk, year=year, month=month,  day=day)
		else:
			print(form.errors.as_data)
			print("something happened")
		return render(request, self.template_name, {'form':form})


	def get(self, request, *args, **kwargs):
		form = CreateLessonForm()
		return render(request, self.template_name, {'form':form})

class CreateLessonSearchView(View):
	template_name= 'lesson/create_lesson_search.html'

	def post(self, request, *args, **kwargs):
		form =  CreateLessonSearchForm(request.POST)
		

		if form.is_valid():
			exercise=Exercise.objects.get(id = self.kwargs['pk'])
			Lesson_det.objects.create( 
				 						cant_max=form.cleaned_data['cant_max'],
				 						quota=form.cleaned_data['cant_max'],
				 						day_lesson=form.cleaned_data['day_lesson'],
										hour_chance=form.cleaned_data['hour'].hour_chance,
				 						hour_lesson=form.cleaned_data['hour'].hour_lesson,
										hour_end=form.cleaned_data['hour'].hour_end,
				 						id_exercise_fk=exercise
				 				     )

			# return HttpResponse("<h1>Todo ok</h1>")
			return redirect('lesson:list_lesson', pk=exercise.id)
		else:
			print(form.errors.as_data)
			print("something happened")
		return render(request, self.template_name, {'form':form})

	def get(self, request, *args, **kwargs):
		week_days = {"Sunday":"domingo", "Monday":"lunes", "Tuesday":"martes", "Wednesday":"miercoles", "Thursday":"jueves", "Friday":"viernes", "Saturday":"sabado"}
		exercise=Exercise.objects.get(id = self.kwargs['pk'])
		fecha_object = datetime.date(self.kwargs['year'], self.kwargs['month'], self.kwargs['day'])
		str_day = fecha_object.strftime("%A")

		form = CreateLessonSearchForm(initial = {'exercise':exercise.name, 'day_lesson':fecha_object})
		form.fields['hour'].queryset = Hour.objects.filter(id_day_fk__name= week_days[str_day], id_exercise_fk=exercise)

		return render(request, self.template_name, {'form':form})

class ListLessonExerciseActionView(View):
	template_name= 'lesson/list_lesson_exercise_action.html'
	context = {}

	def get(self, request, *args, **kwargs):
		exercises = Exercise.objects.all()	
		context = {
						'exercises':exercises
				  }
		return render(request, self.template_name, context)



class ListLessonView(View):
	template_name= 'lesson/list_lesson.html'
	context = {}

	def post(self, request, *args, **kwargs):
		form =  SearchClasses(request.POST)

		if form.is_valid():
			exercise=Exercise.objects.get(id = self.kwargs['pk'])
			lessons = Lesson_det.objects.filter(
													saw=False,
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
		lessons = Lesson_det.objects.filter(saw=False, id_exercise_fk=exercise).order_by("day_lesson")	
		context = {
						'exercise':exercise,
						'lessons':lessons,
						'form':form
				  }

		return render(request, self.template_name, context)

class UpdateLessonView(View):
	template_name= 'lesson/update_lesson.html'
	# paginate_by = 1

	def post(self, request, *args, **kwargs):
		lesson = Lesson_det.objects.get(id=self.kwargs['pk'])

		if lesson.saw == True:
			messages.success(request, 'La clase ya fue vista', extra_tags='alert-danger')
			return redirect('lesson:list_lesson_exercise_action')

		cant_max_before = lesson.cant_max

		form =  UpdateLessonForm(request.POST, instance=lesson)


		if form.is_valid():
			form.save()
			#if the new size of cant_max is less than can_in i delete  all users in the class to re-asign the 'cant_max' of the lesson. 
			if lesson.cant_max < lesson.cant_in:

				users_in_lesson = lesson.id_user_fk.all() #i get all users that are in the lesson		
				for user in users_in_lesson:
					user_exercise_det = Exercise_det.objects.get(id_exercise_fk= lesson.id_exercise_fk, id_user_fk= user)

					user_exercise_det.scheduled_lessons = Lesson_det.objects.filter(id_exercise_fk= lesson.id_exercise_fk, id_user_fk= user, saw= False).exclude(id=lesson.id).count()#here rest to each one in the class -1 before clear the class
					user_exercise_det.saw_lessons = Lesson_det.objects.filter(id_exercise_fk= lesson.id_exercise_fk, id_user_fk= user, saw= True).count()
					user_exercise_det.enable_lessons = user_exercise_det.total_days - (user_exercise_det.saw_lessons + user_exercise_det.bag  + user_exercise_det.scheduled_lessons)
					user_exercise_det.save()

				lesson.id_user_fk.clear() # despues de que les reasigno la cantidad de lecciones que tienen programadas sin tomar en cuenta la lección actual. limpio los usuarios que estén dentro
				lesson.quota = lesson.cant_max
				lesson.cant_in = 0
				lesson.save()
			else:
				lesson.quota = lesson.cant_max - lesson.cant_in
				lesson.save()	
			return redirect('lesson:update_lesson', pk=lesson.id)
		
		return render(request, self.template_name, {'form':form})

	def get(self, request, *args, **kwargs):
		try:
			lesson = Lesson_det.objects.get(id=self.kwargs['pk'])
		except Lesson_det.DoesNotExist:
			messages.success(request, 'La clase que desea manipular fue eliminada o no existe', extra_tags='alert-danger')
			return redirect('lesson:list_lesson_exercise_action')

		if lesson.saw == True:
			messages.success(request, 'La clase ya fue vista', extra_tags='alert-danger')
			return redirect('lesson:list_lesson_exercise_action')


		users_in_lesson = CustomUser.objects.filter(is_active=True, lesson_det__id=lesson.id).order_by('username') 
		all_users = CustomUser.objects.filter(is_active = True, exercise_det__reset=True).order_by('username')
		form = UpdateLessonForm(instance=lesson)

		context={	
					'lesson':lesson,
					'users_in_lesson':users_in_lesson,
					'all_users': all_users,
					'form':form,
				}

		# lesson = Lesson_det.objects.get(id=self.kwargs['pk'])
		# users  = CustomUser.objects.filter(is_active = True).order_by('username')
		# page = self.request.GET.get('page')
		# paginator = Paginator(users, self.paginate_by)
		# page_obj = paginator.get_page(page)
		# form = UpdateLessonForm(instance=lesson)

		# try:
		# 	users = paginator.page(page)
		# except PageNotAnInteger:
		# 	users = paginator.page(1)
		# except EmptyPage:
		# 	users = paginator.page(paginator.num_pages)

		# context={
		# 			'page_obj': page_obj,
		# 			'users': users,
		# 			'form':form,
		# 		}

		return render(request, self.template_name, context)		


class AddToLessonView(View):

	def get(self, request, *args, **kwargs):
		try:
			lesson = Lesson_det.objects.get(id=self.kwargs['id_lesson'])
		except Lesson_det.DoesNotExist:
			messages.success(request, 'La clase que desea manipular fue eliminada o no existe', extra_tags='alert-danger')
			return redirect('lesson:list_lesson_exercise_action')

		if lesson.saw == True:
			messages.success(request, 'La clase ya fue vista', extra_tags='alert-danger')
			return redirect('lesson:list_lesson_exercise_action')

		user = CustomUser.objects.get(id=self.kwargs['id_user']) #obtengo el usuario a agregar a la clase
		#con la clase y el usuario objtengo el exercise_det del usuario para editarlo
		user_exercise_det = Exercise_det.objects.get(id_exercise_fk= lesson.id_exercise_fk.id, id_user_fk= user.id)

		#me aseguro que el usuario no esté en la clase (si no hago esto cuando le de al botón añadir le quita 1 en programadas)
		if Lesson_det.objects.filter(id=lesson.id, id_user_fk=user).count() == 0 and user_exercise_det.enable_lessons > 0: 
			#me aseguro que la cantidad de persona en la clase sea menor que la permitida
			if lesson.cant_in < lesson.cant_max:
				lesson.id_user_fk.add(user)#añado el usuario a la clase
				lesson.cant_in = lesson.id_user_fk.count() #asigno a la cantidad de persona que ahora hay
				lesson.quota = lesson.cant_max - lesson.cant_in #asigno los cupos con una resta
				lesson.save()

				#Esta el la cantidad de clases programadas del usuario
				user_exercise_det.scheduled_lessons = Lesson_det.objects.filter(id_exercise_fk= lesson.id_exercise_fk.id, id_user_fk= user.id, saw= False).count()
				user_exercise_det.saw_lessons = Lesson_det.objects.filter(id_exercise_fk= lesson.id_exercise_fk.id, id_user_fk= user.id, saw= True).count()
				user_exercise_det.enable_lessons = user_exercise_det.total_days - (user_exercise_det.saw_lessons + user_exercise_det.bag  + user_exercise_det.scheduled_lessons)
				user_exercise_det.save()
			
		else:
			#mensajes que paso en el template
			if Lesson_det.objects.filter(id=lesson.id, id_user_fk=user).count() > 0: #si el usuario está en la clase
				messages.success(request, 'El usuario ""{}"" ya está en la clase'.format(user.username), extra_tags='alert-warning')
				

			elif user_exercise_det.enable_lessons == 0: #si el usuario no tiene clases disponibles
				messages.success(request, 'El usuario ""{}"" no tiene días disponibles'.format(user.username), extra_tags='alert-warning')
				
			

		return redirect('lesson:update_lesson', pk=lesson.id)

class TakeOutToLessonView(View):

	def get(self, request, *args, **kwargs):
		try:
			lesson = Lesson_det.objects.get(id=self.kwargs['id_lesson'])
		except Lesson_det.DoesNotExist:
			messages.success(request, 'La clase que desea manipular fue eliminada o no existe', extra_tags='alert-danger')
			return redirect('lesson:list_lesson_exercise_action')

		if lesson.saw == True:
			messages.success(request, 'La clase ya fue vista', extra_tags='alert-danger')
			return redirect('lesson:list_lesson_exercise_action')

		user = CustomUser.objects.get(id=self.kwargs['id_user'])
		user_exercise_det = Exercise_det.objects.get(id_exercise_fk= lesson.id_exercise_fk.id, id_user_fk= user.id)
		
		#me aseguro que el usuario esté en la clase (por seguridad) (esta query es m2m)
		if Lesson_det.objects.filter(id=lesson.id, id_user_fk=user).count() > 0:
			#me aseguro que hayam usuarios en la clase
			if lesson.id_user_fk.count() > 0:
				lesson.id_user_fk.remove(user)#saco al usuario
				lesson.cant_in = lesson.id_user_fk.count()#asigno a la cantidad de persona que ahora hay
				lesson.quota = lesson.cant_max - lesson.cant_in #asigno los cupos con una resta
				lesson.save()

				#Esta el la cantidad de clases programadas del usuario
				user_exercise_det.scheduled_lessons = Lesson_det.objects.filter(id_exercise_fk= lesson.id_exercise_fk.id, id_user_fk= user.id, saw= False).exclude(id=lesson.id).count()
				user_exercise_det.saw_lessons = Lesson_det.objects.filter(id_exercise_fk= lesson.id_exercise_fk.id, id_user_fk= user.id, saw= True).count()
				user_exercise_det.enable_lessons = user_exercise_det.total_days - (user_exercise_det.saw_lessons + user_exercise_det.bag  + user_exercise_det.scheduled_lessons)
				user_exercise_det.save()

		return redirect('lesson:update_lesson', pk=lesson.id)


class SawLessonView(View):

	def get(self, request, *args, **kwargs):
		try:
			lesson = Lesson_det.objects.get(id=self.kwargs['id_lesson'])
		except Lesson_det.DoesNotExist:
			messages.success(request, 'La clase que desea manipular fue eliminada o no existe', extra_tags='alert-danger')
			return redirect('lesson:list_lesson_exercise_action')

		if lesson.saw == True:
			messages.success(request, 'La clase ya fue vista', extra_tags='alert-danger')
			return redirect('lesson:list_lesson_exercise_action')
		
		exercise_id = lesson.id_exercise_fk.id #hago esto por si en un futuro tengo que eliminar la clase despúes de verla
		lesson.saw = True
		lesson.save()

		#Se crea el historial de las personas
		history_obj = History_det.objects.create(
													cant_max = lesson.cant_max,
													cant_in = lesson.cant_in,
													quota = lesson.quota,
													day_lesson = lesson.day_lesson,
													hour_chance = lesson.hour_chance,
													hour_lesson = lesson.hour_lesson,
													hour_end = lesson.hour_end, 
													id_exercise_fk = lesson.id_exercise_fk
												)

		for users_in_lesson in lesson.id_user_fk.all():
			history_obj.id_user_fk.add(users_in_lesson) 
		
			

		users_in_lesson = lesson.id_user_fk.all()
		for user in users_in_lesson:
			user_exercise_det = Exercise_det.objects.get(id_exercise_fk= lesson.id_exercise_fk.id, id_user_fk= user.id)

			#Esta el la cantidad de clases programadas del usuario
			user_exercise_det.enable_lessons = user_exercise_det.total_days - (user_exercise_det.saw_lessons + user_exercise_det.bag  + user_exercise_det.scheduled_lessons)
			user_exercise_det.saw_lessons = Lesson_det.objects.filter(id_exercise_fk= lesson.id_exercise_fk.id, id_user_fk= user.id, saw= True).count()

			user_exercise_det.scheduled_lessons = Lesson_det.objects.filter(id_exercise_fk= lesson.id_exercise_fk.id, id_user_fk= user.id, saw= False).exclude(id=lesson.id).count()
			
			user_exercise_det.save()

		return redirect('lesson:list_lesson', pk=exercise_id)

class DeleteLessonView(View):
	def get(self, request, *args, **kwargs):

		try:
			lesson = Lesson_det.objects.get(id=self.kwargs['id_lesson'])
		except Lesson_det.DoesNotExist:
			messages.success(request, 'La clase que desea manipular fue eliminada o no existe', extra_tags='alert-danger')
			return redirect('lesson:list_lesson_exercise_action')
		
		if lesson.saw == True:
			messages.success(request, 'La clase ya fue vista', extra_tags='alert-danger')
			return redirect('lesson:list_lesson_exercise_action')

		exercise_id= lesson.id_exercise_fk.id
		users_in_lesson = lesson.id_user_fk.all() #i get all users that are in the lesson		
		for user in users_in_lesson:
			user_exercise_det = Exercise_det.objects.get(id_exercise_fk= lesson.id_exercise_fk, id_user_fk= user.id)

			#Esta el la cantidad de clases programadas del usuario
			user_exercise_det.scheduled_lessons = Lesson_det.objects.filter(id_exercise_fk= lesson.id_exercise_fk, id_user_fk= user.id, saw= False).exclude(id=lesson.id).count()#here rest to each one in the class -1 before clear the class
			user_exercise_det.saw_lessons = Lesson_det.objects.filter(id_exercise_fk= lesson.id_exercise_fk, id_user_fk= user.id, saw= True).count()
			user_exercise_det.enable_lessons = user_exercise_det.total_days - (user_exercise_det.saw_lessons + user_exercise_det.bag  + user_exercise_det.scheduled_lessons)
			user_exercise_det.save()

		lesson.delete()

		return redirect('lesson:list_lesson', pk=exercise_id)