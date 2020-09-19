#shortcuts
from django.shortcuts import render, redirect
from django.http import HttpResponse

#models
from apps.exercise.models import Exercise, Hour
from apps.exercise_det.models import Exercise_det, update_resumen
from apps.create_user.models import CustomUser
from apps.devolution.models import Devolution
from .models import Lesson_det

#views
from django.views import View

#forms
from .forms import ( 
					 CreateLessonForm, CreateLessonSearchForm,
				     SearchClassesForm, UpdateLessonForm 
				    )

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib import messages
import datetime



#------------------------------------------------------------------------------------------
#lesson
#------------------------------------------------------------------------------------------
class CreateLessonView(View):
	"""
		in this class i pass by the post method the date selected in the form to another view by a url
	"""
	template_name= 'lesson/create_lesson.html'

	def post(self, request, *args, **kwargs):
		form =  CreateLessonForm(request.POST)

		if form.is_valid():
			pk=self.kwargs['id_exercise']
			year=form.cleaned_data['day_lesson'].year
			month=form.cleaned_data['day_lesson'].month
			day=form.cleaned_data['day_lesson'].day
			# return HttpResponse("<h1>Todo ok</h1>")

			return redirect('lesson:create_lesson_form_search', id_exercise=pk, year=year, month=month,  day=day)
		else:
			print(form.errors.as_data)
			print("something happened")
		return render(request, self.template_name, {'form':form})


	def get(self, request, *args, **kwargs):
		#validacion de que sea un superusuario
		if not request.user.is_superuser:
			return redirect('admin_login:login_admin')

		form = CreateLessonForm()
		return render(request, self.template_name, {'form':form})

class CreateLessonSearchView(View):
	"""
		En esta clase creo una lección con los datos pasados por el url(es una fecha).
		En el metodo "get": recibo la fecha por el url y creo un objeto tipo date. luego se lo asigno al formulario y utilizo
		la fecha para ver cuales son las horas disponibles para ese día.
		En el metodo "post": creo el objeto lesson con los datos sumenistrados. 
	"""
	template_name= 'lesson/create_lesson_search.html'

	def post(self, request, *args, **kwargs):
		form =  CreateLessonSearchForm(request.POST)
		

		if form.is_valid():
			try:
				exercise=Exercise.objects.get(id = self.kwargs['id_exercise'])
			except Exercise.DoesNotExist:
				messages.success(request, 'El ejercicio fue eliminado o no existe', extra_tags='alert-danger')
				return redirect('lesson:list_lesson_exercise_action')

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
			messages.success(request, 'La clase fue creada con éxito', extra_tags='alert-success')
			return redirect('lesson:list_lesson', id_exercise=exercise.id)
		else:
			print(form.errors.as_data)
			print("something happened")
		return render(request, self.template_name, {'form':form})

	def get(self, request, *args, **kwargs):
		#validacion de que sea un superusuario
		if not request.user.is_superuser:
			return redirect('admin_login:login_admin')


		week_days = {"Sunday":"domingo", "Monday":"lunes", "Tuesday":"martes", "Wednesday":"miercoles", "Thursday":"jueves", "Friday":"viernes", "Saturday":"sabado"}
		try:
			exercise=Exercise.objects.get(id = self.kwargs['id_exercise'])
		except Exercise.DoesNotExist:
			messages.success(request, 'El ejercicio fue eliminado o no existe', extra_tags='alert-danger')
			return redirect('lesson:list_lesson_exercise_action')

		fecha_object = datetime.date(self.kwargs['year'], self.kwargs['month'], self.kwargs['day'])
		str_day = fecha_object.strftime("%A") #obtengo el día sumistrado en ingles

		form = CreateLessonSearchForm(initial = {'exercise':exercise.name, 'day_lesson':fecha_object})
		form.fields['hour'].queryset = Hour.objects.filter(id_day_fk__name= week_days[str_day], id_exercise_fk=exercise) #convierto el día de español seleccionado a inglés

		return render(request, self.template_name, {'form':form})

class ListLessonExerciseActionView(View):
	template_name= 'lesson/list_lesson_exercise_action.html'
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



class ListLessonView(View):
	template_name= 'lesson/list_lesson.html'
	context = {}

	def post(self, request, *args, **kwargs):
		form =  SearchClassesForm(request.POST)

		if form.is_valid():
			try:
				exercise=Exercise.objects.get(id = self.kwargs['id_exercise'])
			except Exercise.DoesNotExist:
				messages.success(request, 'El ejercicio fue eliminado o no existe', extra_tags='alert-danger')
				return redirect('lesson:list_lesson_exercise_action')

			lessons = Lesson_det.objects.filter(	
													reset = False,
												    id_exercise_fk=exercise,
												    day_lesson__range=(form.cleaned_data['since'],form.cleaned_data['until'])
												    
												).exclude(lesson_status = Lesson_det.FINISHED).order_by("day_lesson", "hour_lesson")	
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

			try:
				exercise=Exercise.objects.get(id = self.kwargs['id_exercise'])
			except Exercise.DoesNotExist:
				messages.success(request, 'El ejercicio fue eliminado o no existe', extra_tags='alert-danger')
				return redirect('lesson:list_lesson_exercise_action')

			lessons = Lesson_det.objects.filter(reset = False, id_exercise_fk=exercise).exclude(lesson_status = Lesson_det.FINISHED).order_by("day_lesson", "hour_lesson")	
			context = {
							'exercise':exercise,
							'lessons':lessons,
							'form':form
					  }

		return render(request, self.template_name, context)

	def get(self, request, *args, **kwargs):
		#validacion de que sea un superusuario
		if not request.user.is_superuser:
			return redirect('admin_login:login_admin')

		form = SearchClassesForm()

		try:
			exercise=Exercise.objects.get(id = self.kwargs['id_exercise'])
		except Exercise.DoesNotExist:
			messages.success(request, 'El ejercicio fue eliminado o no existe', extra_tags='alert-danger')
			return redirect('lesson:list_lesson_exercise_action')

		lessons = Lesson_det.objects.filter(reset = False, id_exercise_fk=exercise).exclude(lesson_status = Lesson_det.FINISHED).order_by("day_lesson", "hour_lesson")	
		context = {
						'exercise':exercise,
						'lessons':lessons,
						'form':form
				  }

		return render(request, self.template_name, context)

class UpdateLessonView(View):
	"""
		In this class i pass the users that are in the class,  and i pass all users too to make a search between users.
		I pass a form to update the date of the class, cant_max and time. The scritp that searches the users at the moment is 
		in the template.
	"""

	template_name= 'lesson/update_lesson.html'
	# paginate_by = 1

	def post(self, request, *args, **kwargs):
		try:
			lesson = Lesson_det.objects.get(id=self.kwargs['pk'])
		except Lesson_det.DoesNotExist:
			messages.success(request, 'La clase que desea manipular fue eliminada o no existe', extra_tags='alert-danger')
			return redirect('lesson:list_lesson_exercise_action')

		if lesson.lesson_status == Lesson_det.FINISHED:
			messages.success(request, 'La clase ya fue vista', extra_tags='alert-danger')
			return redirect('lesson:list_lesson_exercise_action')

		form =  UpdateLessonForm(request.POST, instance=lesson)

		if form.is_valid():
			form.save() #update only if administrator enters new value to cant_max
			#if the new size of cant_max is less than can_in i delete  all users in the class to re-asign the 'cant_max' of the lesson. 
			if lesson.cant_max < lesson.cant_in:
				lesson.id_user_fk.clear() #after I reassign them the number of lessons they have scheduled regardless of the current lesson. I clean the users that are inside
			return redirect('lesson:update_lesson', pk=lesson.id)
		
		return render(request, self.template_name, {'form':form})

	def get(self, request, *args, **kwargs):
		#validacion de que sea un superusuario
		if not request.user.is_superuser:
			return redirect('admin_login:login_admin')

		try:
			lesson = Lesson_det.objects.get(id=self.kwargs['pk'])
		except Lesson_det.DoesNotExist:
			messages.success(request, 'La clase que desea manipular fue eliminada o no existe', extra_tags='alert-danger')
			return redirect('lesson:list_lesson_exercise_action')

		if lesson.lesson_status == Lesson_det.FINISHED:
			messages.success(request, 'La clase ya fue vista', extra_tags='alert-danger')
			return redirect('lesson:list_lesson_exercise_action')


		#usuarios que están en la clase
		users_in_lesson = CustomUser.objects.filter(
														is_active=True, 
														lesson_det__id=lesson.id
													).order_by('username')
		#usuarios que están en devoluciones
		users_devolution = CustomUser.objects.filter(
														devolution__id_lesson_fk__id=lesson.id
													)
		#declaro la variable users_list  para no afecta a los usuarios de la lección al momento de hacer la unión.
		#ya que se necesita en el template
		users_list = users_in_lesson
		users_list = users_list.union(users_devolution).values('id')

		all_users = CustomUser.objects.filter(
			 									is_active = True,
			 									exercise_det__id_exercise_fk=lesson.id_exercise_fk,
			 									exercise_det__reset=True
			 								  ).order_by('username').exclude(id__in=users_list)

		form = UpdateLessonForm(instance=lesson)

		context={	
					'lesson':lesson,
					'users_in_lesson':users_in_lesson,
					'users_devolution':users_devolution,
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
	"""
		This class adds a user to lesson.
		if the user is in the class already, a warning is thrown.
		Restriction: To add the user, the user have to have enable days-
	"""
	def get(self, request, *args, **kwargs):
		#validacion de que sea un superusuario
		if not request.user.is_superuser:
			return redirect('user_exercise_det:login_admin')

		try:
			lesson = Lesson_det.objects.get(id=self.kwargs['id_lesson'])
		except Lesson_det.DoesNotExist:
			messages.success(request, 'La clase que desea manipular fue eliminada o no existe', extra_tags='alert-danger')
			return redirect('lesson:list_lesson_exercise_action')

		if lesson.lesson_status == Lesson_det.FINISHED:
			messages.success(request, 'La clase ya fue vista', extra_tags='alert-danger')
			return redirect('lesson:list_lesson_exercise_action')

		try:
			user = CustomUser.objects.get(id=self.kwargs['id_user'])
		except CustomUser.DoesNotExist:
			messages.success(request, 'El usuario fue eliminado', extra_tags='alert-danger')
			return redirect('devolution:update_devolution', id_lesson=self.kwargs['id_lesson'])

		user_exercise_det = Exercise_det.objects.get(id_exercise_fk=lesson.id_exercise_fk, id_user_fk=user)

		#verifico que el usuario a agregar no esté en la clase
		no_in_class = Lesson_det.objects.filter(id=lesson.id, id_user_fk=self.kwargs['id_user']).count() == 0

		#verifico que el usuario no esté en las devoluciones
		no_in_devolution = Devolution.objects.filter(id_lesson_fk=lesson.id, id_user_fk=self.kwargs['id_user']).count() == 0

		#verifico que el usuario tenga días disponibles, si no hago esto le resta uno a los días disponibles y coloca en negativo
		has_lesson = user_exercise_det.enable_lessons > 0

		if no_in_class and no_in_devolution and has_lesson:
			if lesson.cant_in < lesson.cant_max:
				lesson.id_user_fk.add(user)#añado el usuario a la clase


		elif no_in_class == False:
			messages.success(request, 'El usuario ""{}"" ya está en la clase'.format(user.username), extra_tags='alert-warning')

		elif no_in_devolution == False:				
			messages.success(request, 'El usuario ""{}"" ya está en devoluciones'.format(user.username), extra_tags='alert-warning')	

		elif user_exercise_det.enable_lessons == 0:
			messages.success(request, 'El usuario ""{}"" no tiene días disponibles'.format(user.username), extra_tags='alert-warning')
		
		
			
		return redirect('lesson:update_lesson', pk=lesson.id)

class TakeOutToLessonView(View):
	"""
		This class takes some out of lesson.
	"""
	def get(self, request, *args, **kwargs):
		#validacion de que sea un superusuario
		if not request.user.is_superuser:
			return redirect('admin_login:login_admin')

		try:
			lesson = Lesson_det.objects.get(id=self.kwargs['id_lesson'])
		except Lesson_det.DoesNotExist:
			messages.success(request, 'La clase que desea manipular fue eliminada o no existe', extra_tags='alert-danger')
			return redirect('lesson:list_lesson_exercise_action')

		if lesson.lesson_status == Lesson_det.FINISHED:
			messages.success(request, 'La clase ya fue vista', extra_tags='alert-danger')
			return redirect('lesson:list_lesson_exercise_action')

		try:
			user =	CustomUser.objects.get(id=self.kwargs['id_user'])
		except CustomUser.DoesNotExist:
			messages.success(request, 'El usuario fue eliminado', extra_tags='alert-danger')
			return redirect('devolution:update_devolution', id_lesson=self.kwargs['id_lesson'])
		
		#me aseguro que el usuario esté en la clase (por seguridad) (esta query es m2m)
		if Lesson_det.objects.filter(id=lesson.id, id_user_fk=user).count() > 0:
			#me aseguro que hayan usuarios en la clase
			if lesson.id_user_fk.count() > 0:
				lesson.id_user_fk.remove(user)#saco al usuario

		return redirect('lesson:update_lesson', pk=lesson.id)

class TakeOutToUsersDevolutionView(View):
	"""
		This class takes some devolution out  of the lesson
	"""
	def get(self, request, *args, **kwargs):
		#validacion de que sea un superusuario
		if not request.user.is_superuser:
			return redirect('admin_login:login_admin')

		try:
			lesson = Lesson_det.objects.get(id=self.kwargs['id_lesson'])
		except Lesson_det.DoesNotExist:
			messages.success(request, 'La clase que desea manipular fue eliminada o no existe', extra_tags='alert-danger')
			return redirect('lesson:list_lesson_exercise_action')

		if lesson.lesson_status == Lesson_det.FINISHED:
			messages.success(request, 'La clase ya fue vista', extra_tags='alert-danger')
			return redirect('lesson:list_lesson_exercise_action')

		try:
			CustomUser.objects.get(id=self.kwargs['id_user'])
		except CustomUser.DoesNotExist:
			messages.success(request, 'El usuario fue eliminado', extra_tags='alert-danger')
			return redirect('devolution:update_devolution', id_lesson=self.kwargs['id_lesson'])

		devolution = Devolution.objects.filter( 
											 	id_user_fk = self.kwargs['id_user'],
											 	id_lesson_fk=self.kwargs['id_lesson']
											   ).first()

		if devolution == None:
			messages.success(request, 'El usuario no están', extra_tags='alert-danger')
			return redirect('devolution:update_devolution', id_lesson=self.kwargs['id_lesson'])

		devolution.id_lesson_fk.remove(lesson)

		return redirect('lesson:update_lesson', pk=lesson.id)

class SawLessonView(View):
	"""
		This class puts a lesson in the status "FINISHED" and creates its history
	"""
	def get(self, request, *args, **kwargs):
		#validacion de que sea un superusuario
		if not request.user.is_superuser:
			return redirect('admin_login:login_admin')

		try:
			lesson = Lesson_det.objects.get(id=self.kwargs['id_lesson'])
		except Lesson_det.DoesNotExist:
			messages.success(request, 'La clase que desea manipular fue eliminada o no existe', extra_tags='alert-danger')
			return redirect('lesson:list_lesson_exercise_action')

		if lesson.lesson_status == Lesson_det.FINISHED:
			messages.success(request, 'La clase ya fue vista', extra_tags='alert-danger')
			return redirect('lesson:list_lesson_exercise_action')
		
		#putting up the lesson en finished status
		lesson.lesson_status = Lesson_det.FINISHED
		lesson.save()

		#obteniendo todas la devoluciones que apuntan a la lección para colocarlas como entregadas en tal caso que hayan
		associated_devolutions = lesson.devolution_set.all()

		for associated_devolution in associated_devolutions:
			associated_devolution.returned = True
			associated_devolution.save()

		return redirect('lesson:list_lesson', id_exercise=lesson.id_exercise_fk.id)

class DeleteLessonView(View):
	"""
		Here i delete the lesson when the button is pressed
	"""
	def get(self, request, *args, **kwargs):
		#validacion de que sea un superusuario
		if not request.user.is_superuser:
			return redirect('admin_login:login_admin')
			
		try:
			lesson = Lesson_det.objects.get(id=self.kwargs['id_lesson'])
		except Lesson_det.DoesNotExist:
			messages.success(request, 'La clase que desea manipular fue eliminada o no existe', extra_tags='alert-danger')
			return redirect('lesson:list_lesson_exercise_action')
		
		if lesson.lesson_status == Lesson_det.FINISHED:
			messages.success(request, 'La clase ya fue vista', extra_tags='alert-danger')
			return redirect('lesson:list_lesson_exercise_action')


		exercise_id=lesson.id_exercise_fk.id
		lesson.id_user_fk.clear()
		lesson.delete()

		return redirect('lesson:list_lesson', id_exercise=exercise_id)


class DevolutionLessonView(View):
	"""
		Here i create a devolution when the button is pressed
	"""
	def get(self, request, *args, **kwargs):
		#validacion de que sea un superusuario
		if not request.user.is_superuser:
			return redirect('admin_login:login_admin')

		lesson = None
		

		try:
			lesson = Lesson_det.objects.get(id=self.kwargs['id_lesson'])
		except Lesson_det.DoesNotExist:
			messages.success(request, 'La clase que desea manipular fue eliminada o no existe', extra_tags='alert-danger')
			return redirect('history:list_history', id_exercise=lesson.id_exercise_fk.id)
		
		if Devolution.objects.filter(id_lesson_before = lesson.id).count() > 0:
			messages.success(request, 'Ya ha sido creada la devolución de esta clase', extra_tags='alert-danger')
			return redirect('history:list_history', id_exercise=lesson.id_exercise_fk.id)

		if lesson.lesson_status == Lesson_det.FINISHED:
						
			#usuarios de la clase
			users = lesson.id_user_fk.all()

			#usuarios en la devolucion
			users = users.union(CustomUser.objects.filter(devolution__id_lesson_fk= lesson.id))
			
			for user in users: 
				devolution = Devolution.objects.create(

											id_exercise_fk = lesson.id_exercise_fk,

											day_lesson = lesson.day_lesson,
											hour_chance = lesson.hour_chance,
											hour_lesson = lesson.hour_lesson,
											hour_end = lesson.hour_end,

											cant_max = lesson.cant_max, 
											cant_in = lesson.cant_in,

											id_user_fk = user
											)

				devolution.id_lesson_before = lesson.id #este es el id de la leccion que creó la devolución
				devolution.save()
			
			messages.success(request, 'Se han creado con exito las devoluciones', extra_tags='alert-success')
		else:
			messages.success(request, 'La clase que quiere manipular no está en modo finalizado', extra_tags='alert-danger')

		return redirect('history:list_history', id_exercise=lesson.id_exercise_fk.id)