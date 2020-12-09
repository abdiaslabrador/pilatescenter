#shortcuts
from django.shortcuts import render, redirect
from django.http import  HttpResponse

#models
from apps.plan.models import Plan
from apps.exercise.models import Exercise
from apps.exercise_det.models import Exercise_det, update_resumen
from apps.lesson_det.models import Lesson_det
from apps.devolution.models import Devolution
from .models import CustomUser

#views
from django.views.generic.list import ListView
from django.views import View
from django.contrib import messages

#forms
from .forms import ( 
						UserCreationForm, ChangePasswordForm,
						 UserUpdateForm
					)

from apps.exercise_det.forms import ( 
									  ConfigurationUserExerciseForm, ConfigurationUserChangePlanForm,
									  ConfigurationUserResetForm
									)
from apps.lesson_det.forms import SearchClassesForm

#django rest-rest_framework
from django.core import serializers
from .serializers import CustomUserSeliazer
from rest_framework.serializers import  ModelSerializer
import json
from rest_framework.views import  APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication




#------------------------------------------------------------------------------------------
#user
#------------------------------------------------------------------------------------------

class ListUserView(View):
	"""this function is to list all users in the admin page"""
	template_name = 'users/list_users.html'

	def get(self, request, *args, **kwargs):
		#validacion de que sea un superusuario
		if not request.user.is_superuser:
			return redirect('admin_login:login_admin')

		users = CustomUser.objects.filter(is_active=True).order_by("username")
		context={
				'users':users,
			 }

		return render(request, self.template_name, context)

class ListLockedUserView(View):
	"""here i show all the locked users"""
	template_name = 'users/locked_users.html'

	def get(self, request, *args, **kwargs):
		#validacion de que sea un superusuario
		if not request.user.is_superuser:
			return redirect('admin_login:login_admin')

		users = CustomUser.objects.filter(is_active=False).order_by("username")
		context={
					'users':users,
				}

		return render(request, self.template_name, context)

#locking a  user
class LockUserView(View):
	"""here i lock a user when the button "Bloquear" is pressed in the list users """

	def get(self, request, *args, **kwargs):
		#validacion de que sea un superusuario
		if not request.user.is_superuser:
			return redirect('admin_login:login_admin')

		try:
			user = CustomUser.objects.get(id = self.kwargs['pk'])
		except CustomUser.DoesNotExist:
			messages.success(request, 'El usuario fue eliminado o no existe', extra_tags='alert-danger')
			return redirect('content_user:list_locked_user')

		if Lesson_det.objects.filter(id_user_fk= user).exclude(lesson_status = Lesson_det.FINISHED).count() > 0:
			messages.success(self.request, 'No se puede bloquear un usuario con clases programadas', extra_tags='alert-danger')
			return redirect('content_user:list_user')

		user.is_active=False
		user.save()
		return redirect('content_user:list_user')

#unloking a user
class  UnlockUserView(View):
	
	def get(self, request, *args, **kwargs):
		#validacion de que sea un superusuario
		if not request.user.is_superuser:
			return redirect('admin_login:login_admin')

		try:
			user = CustomUser.objects.get(id = self.kwargs['pk'])
		except CustomUser.DoesNotExist:
			messages.success(request, 'El usuario fue eliminado o no existe', extra_tags='alert-danger')
			return redirect('content_user:list_locked_user')

		user.is_active=True
		user.save()
		return redirect('content_user:list_locked_user')


#Creating a user
def create_user(request):
	"""this form creates a user which has a signal in exercise_det model"""
	if request.method == 'POST':
		form = UserCreationForm(request.POST)
		if form.is_valid():
			form.save()
			print("ES VALIDO!")
			return redirect('content_user:list_user')
		else:
			print("es invalido chao!")
	else:
		#validacion de que sea un superusuario
		if not request.user.is_superuser:
			return redirect('admin_login:login_admin')
		form = UserCreationForm()

	return render(request,'users/create_user.html', {'form':form})

#Updating a user
def modific_user(request, pk):
	"""
		this  form  modifies a user. In the below of the page is presented
		all exercise that the business offer.
	"""
	try:
		user=CustomUser.objects.get(pk=pk)
	except CustomUser.DoesNotExist:
		messages.success(request, 'El usuario fue eliminado o no existe', extra_tags='alert-danger')
		return redirect('content_user:list_user')
		
	exercises_det = Exercise_det.objects.filter(id_user_fk = user).order_by('name')

	if request.method == 'GET':
		#validacion de que sea un superusuario
		if not request.user.is_superuser:
			return redirect('admin_login:login_admin')

		form = UserUpdateForm(instance=user, initial={'primarykey': user.pk})#i use the primary key to validate the username modificated whit the other usernames registered

	else:
		form = UserUpdateForm(request.POST, instance=user)
		if form.is_valid():
			form.save()
			# print("ES VALIDO!")
			return redirect('content_user:list_user')
		# else: #si el formuñario no esválido, esto es para pruebas
		# 	# print("NO es invalido chao!")
		# 	return render(request,'users/modific_user.html', {'form':form})
	contexto={
				'form':form,
				'exercises_det_list': exercises_det,
				'user_to_modific':user,
			 }
	return render(request,'users/modific_user.html', contexto)

#Changing the user password
def change_password_user(request, pk):
	"""This form is located inside of the modific user part"""
	
	try:
		user=CustomUser.objects.get(pk=pk)
	except CustomUser.DoesNotExist:
		messages.success(request, 'El usuario fue eliminado o no existe', extra_tags='alert-danger')
		return redirect('content_user:list_user')

	if request.method == 'POST':
		form = ChangePasswordForm(request.POST)
		if form.is_valid():
			# print("ES VALIDO!" + " " + form.cleaned_data['password'])
			user.set_password(form.cleaned_data['password'])
			user.save()
			return redirect('content_user:list_user')
		# else:
			# print("NO es invalido chao!")
	else:
		#validacion de que sea un superusuario
		if not request.user.is_superuser:
			return redirect('admin_login:login_admin')

		form = ChangePasswordForm()
		context = {
					'form':form,
					'user':user,
		}
	return render(request,'users/change_password_user.html', context)


#deleting a user
class DeleteUserView(View):
	"""
		This function deletes the user when the delete button in the list of user is pressed.
		The condition to delete a user is: a user cannot has a least one lesson scheduled
	"""
	def get(self, request, *args, **kwargs):

		#validacion de que sea un superusuario
		if not request.user.is_superuser:
			return redirect('admin_login:login_admin')

		try:
			user = CustomUser.objects.get(pk=self.kwargs['pk'])
		except CustomUser.DoesNotExist:
			messages.success(request, 'EL usuario fue eliminado o no existe', extra_tags='alert-danger')
			return redirect('content_user:list_user')

		if Lesson_det.objects.filter(id_user_fk= user).exclude(lesson_status = Lesson_det.FINISHED).count() > 0:
			messages.success(self.request, 'No se puede eliminar un usuario con clases programadas', extra_tags='alert-danger')
			return redirect('content_user:list_user')

		user.delete()
		return redirect('content_user:list_user')



#reset a user
class ResetUsersView(View):
	"""
		here i reset all users when  the button is pressed that had the exercise specified
		The condition to reset a user is: a user cannot has at least one lesson scheduled
	"""
	def get(self, request, *args, **kwargs):

		#validacion de que sea un superusuario
		if not request.user.is_superuser:
			return redirect('admin_login:login_admin')
		
		try:
			exercise = Exercise.objects.get(pk=self.kwargs['pk'])
		except Exercise.DoesNotExist:
			messages.success(request, 'El ejercicio fue eliminado o no existe', extra_tags='alert-danger')
			return redirect('exercise:list_exercise')

		#esto es para verificar que no hayan usuarios con clases programadas para hacer el reinicio
		lessons = Lesson_det.objects.filter(	
												reset= False,
												id_exercise_fk=exercise
											).exclude(lesson_status = Lesson_det.FINISHED).exclude(id_user_fk = None).count()

		if lessons > 0:
			messages.success(self.request, 'Hay almenos una clase con usuarios dentro. No se puede reinicar un ejercicio con usuarios en clases', extra_tags='alert-danger')
			return redirect('exercise:list_exercise')

		#esto es para verificar que no hayan devoluciones en clases, para poder hacer el reinicio
		devolutions = Devolution.objects.filter(	
												returned= False,
												id_exercise_fk=exercise
											).exclude(id_lesson_fk = None).count()

		if devolutions > 0:
			messages.success(self.request, 'Hay almenos una clase con devoluciones dentro. No se puede reiniciar un ejercicio con usuarios en la clase', extra_tags='alert-danger')
			return redirect('exercise:list_exercise')

		#obtengo todos los exercise_det de los usuarios con el respectivo ejercicio que se puedan reiniciar
		exercises_det = Exercise_det.objects.filter(id_exercise_fk=exercise)
		for exercise_det in exercises_det:
			exercise_det.resetter()


		messages.success(self.request, 'Se han reiniciado los usuarios', extra_tags='alert-success')
		return redirect('exercise:list_exercise')

#------------------------------------------------------------------------------------------
#setting up the user. This part is inside the user modification table
#------------------------------------------------------------------------------------------
#this class work when the "ver" button is pressed
class UserConfigurationClassView(View):
	"""
		In this class i show:
		 - table with all classes that a user haven't seen yet of specific user with a date filter.
	"""
	template_name= 'users/user_configuration/table_lesson.html'

	def post(self, request, *args, **kwargs):
		
		try:
			exercise_det = Exercise_det.objects.get(pk=self.kwargs['pk'])
		except Exercise_det.DoesNotExist:
			messages.success(request, 'El ejercicio fue eliminado o no existe', extra_tags='alert-danger')
			return redirect('content_user:list_user')		

		try:
			user_to_modific = CustomUser.objects.get(exercise_det__id = self.kwargs['pk'])
		except CustomUser.DoesNotExist:
			messages.success(request, 'El usuario fue eliminado o no existe', extra_tags='alert-danger')
			return redirect('content_user:list_user')

		form =  SearchClassesForm(request.POST)

		if form.is_valid():
			
			lessons = Lesson_det.objects.filter(
													reset = False,
													day_lesson__range=(form.cleaned_data['since'],form.cleaned_data['until']),
												    id_exercise_fk=exercise_det.id_exercise_fk.id,
												    id_user_fk=user_to_modific.id
												).exclude(lesson_status = Lesson_det.FINISHED)

			#devoluciones del usuario
			lesson_devolution = Lesson_det.objects.filter(
														reset = False,
														devolution__id_user_fk__id =  user_to_modific.id,
														id_exercise_fk = exercise_det.id_exercise_fk.id,
														day_lesson__range=(form.cleaned_data['since'],form.cleaned_data['until']),
												   ).exclude(lesson_status = Lesson_det.FINISHED)

			lessons = lessons.union(lesson_devolution).order_by("day_lesson", "hour_lesson")

			context = {	
						'form':form,
						'exercise_det' : exercise_det,
						'user_to_modific': user_to_modific,
						'lessons':lessons,
						
				       }
			# return HttpResponse("<h1>Todo ok</h1>")
			return render(request, self.template_name, context)
		else:
			print(form.errors.as_data)
			print("something happened")

			lessons = Lesson_det.objects.filter(	reset = False,
													id_exercise_fk=exercise_det.id_exercise_fk.id, 
													id_user_fk=user_to_modific.id
												).exclude(lesson_status = Lesson_det.FINISHED)

			#devoluciones del usuario
			lesson_devolution = Lesson_det.objects.filter(
														reset = False,
														devolution__id_user_fk__id =  user_to_modific.id,
														id_exercise_fk = exercise_det.id_exercise_fk.id,
												   ).exclude(lesson_status = Lesson_det.FINISHED)

			lessons = lessons.union(lesson_devolution).order_by("day_lesson", "hour_lesson")

			context = {	
						'form':form,
						'exercise_det' : exercise_det,
						'user_to_modific': user_to_modific,
						'lessons':lessons,
				       }

		return render(request, self.template_name, context)

	def get(self, request, *args, **kwargs):
		#validacion de que sea un superusuario
		if not request.user.is_superuser:
			return redirect('admin_login:login_admin')

		form = SearchClassesForm()

		try:
			exercise_det = Exercise_det.objects.get(pk=self.kwargs['pk'])
		except Exercise_det.DoesNotExist:
			messages.success(request, 'El ejercicio fue eliminado o no existe', extra_tags='alert-danger')
			return redirect('content_user:list_user')		

		try:
			user_to_modific = CustomUser.objects.get(exercise_det__id = self.kwargs['pk'])
		except CustomUser.DoesNotExist:
			messages.success(request, 'El usuario fue eliminado o no existe', extra_tags='alert-danger')
			return redirect('content_user:list_user')

		lessons = Lesson_det.objects.filter(	reset = False,
													id_exercise_fk=exercise_det.id_exercise_fk.id, 
													id_user_fk=user_to_modific.id
												).exclude(lesson_status = Lesson_det.FINISHED)

		#devoluciones del usuario
		lesson_devolution = Lesson_det.objects.filter(
													reset = False,
													devolution__id_user_fk__id =  user_to_modific.id,
													id_exercise_fk = exercise_det.id_exercise_fk.id,
											   ).exclude(lesson_status = Lesson_det.FINISHED)

		lessons = lessons.union(lesson_devolution).order_by("day_lesson", "hour_lesson")

		context = {	
						'form':form,
						'exercise_det' : exercise_det,
						'user_to_modific': user_to_modific,
						'lessons':lessons,
				   }
		return render(request, self.template_name, context)

#this class work when the "saw" button is pressed
class UserConfigurationSawLessonView(View):
	"""
		In this class i put a particular lesson as saw and update his summary too. Once i did it, 
		i create a history with the lesson datas.
	"""
	def get(self, request, *args, **kwargs):

		#validacion de que sea un superusuario
		if not request.user.is_superuser:
			return redirect('admin_login:login_admin')

		try:
			lesson = Lesson_det.objects.get(id=self.kwargs['id_lesson'])
		except Lesson_det.DoesNotExist:
			messages.success(request, 'La clase que desea manipular fue eliminada o no existe', extra_tags='alert-danger')
			return redirect('content_user:user_configuration_class', pk=self.kwargs['id_exercise_det'])

		if lesson.lesson_status == Lesson_det.FINISHED:
			messages.success(request, 'La clase ya fue vista', extra_tags='alert-danger')
			return redirect('content_user:user_configuration_class', pk=self.kwargs['id_exercise_det'])
		
		
		lesson.lesson_status = Lesson_det.FINISHED
		lesson.save()
		# update_resumen(lesson)#this function updates the "summary" of the exercise related to the lesson, and is located in model of the exercise_det app

		return redirect('content_user:user_configuration_class', pk=self.kwargs['id_exercise_det'])
		
class DeleteLessonView(View):
	"""
		here i delete a particular user lesson and after to do this i update the summary
	"""
	def get(self, request, *args, **kwargs):
		#validacion de que sea un superusuario
		if not request.user.is_superuser:
			return redirect('admin_login:login_admin')

		try:
			lesson = Lesson_det.objects.get(id=self.kwargs['id_lesson'])
		except Lesson_det.DoesNotExist:
			messages.success(request, 'La clase que desea manipular fue eliminada o no existe', extra_tags='alert-danger')
			return redirect('content_user:user_configuration_class', pk=self.kwargs['id_exercise_det'])	

		if lesson.lesson_status == Lesson_det.FINISHED:
			messages.success(request, 'La clase ya fue vista', extra_tags='alert-danger')
			return redirect('content_user:user_configuration_class', pk=self.kwargs['id_exercise_det'])	
			
		update_resumen(lesson)#this function updates the "summary" of the exercise related to the lesson, and is located in model of the exercise_det app

		lesson.delete()#this method has a signal in the exercise_det model

		return redirect('content_user:user_configuration_class', pk=self.kwargs['id_exercise_det'])

#the class that manage the summary status
class UserConfigurationResumenView(View):
	"""
		Here i show the summary of a particular user.
		the form of this class is located in the exercise_det forms. 
	"""
	template_name = 'users/user_configuration/resumen.html'
	context = {}

	def post(self, request, *args, **kwargs):

		try:
			exercise_det = Exercise_det.objects.get(pk=self.kwargs['pk'])
		except Exercise_det.DoesNotExist:
			messages.success(request, 'El ejercicio fue eliminado o no existe', extra_tags='alert-danger')
			return redirect('content_user:list_user')		

		try:
			user_to_modific = CustomUser.objects.get(exercise_det__id = self.kwargs['pk'])
		except CustomUser.DoesNotExist:
			messages.success(request, 'El usuario fue eliminado o no existe', extra_tags='alert-danger')
			return redirect('content_user:list_user')

		form = ConfigurationUserExerciseForm(request.POST, instance=exercise_det)

		#this "if" is part of a validation of reset condition of the user
		if exercise_det.reset == True:
			if form.is_valid():
				form.save()
				
				user_exercise_det = Exercise_det.objects.get(id_exercise_fk= exercise_det.id_exercise_fk, id_user_fk= user_to_modific)
				

				user_exercise_det.devolutions = Devolution.objects.filter(	
														returned = False,
														id_user_fk = user_to_modific,
														id_lesson_fk = None,
														id_exercise_fk= exercise_det.id_exercise_fk,
													).count()

				user_exercise_det.scheduled_lessons = Lesson_det.objects.filter(	
																					reset=False,
																					id_exercise_fk= exercise_det.id_exercise_fk,
																					id_user_fk= user_to_modific
																				).exclude(lesson_status = Lesson_det.FINISHED).count()

				user_exercise_det.saw_lessons = Lesson_det.objects.filter(
																			reset=False,
																			lesson_status = Lesson_det.FINISHED,
																			id_exercise_fk= exercise_det.id_exercise_fk,
																			id_user_fk= user_to_modific
																		).count()

				user_exercise_det.enable_lessons = user_exercise_det.total_days - (user_exercise_det.saw_lessons + user_exercise_det.bag  + user_exercise_det.scheduled_lessons)
				user_exercise_det.save()
				# print("Este es la data" + str(form.cleaned_data))
				# print("ES VALIDO!")
				return redirect('content_user:user_configuration_class', pk=self.kwargs['pk'])
			else:
				print("no es válido")
				self.context = {
									'form':form,
									'user_to_modific': user_to_modific,
									'exercise_det': exercise_det,
							
					   }
			return render(request, self.template_name, self.context)

		elif exercise_det.reset == False: #esto es por si intenta modificar un usuario que ya ha fue previamente colocado en modo "No reiniciar"
			messages.success(self.request, 'No se han guardado cambios porque previamente ha activado la opción de "No reiniciar"', extra_tags='alert-danger')
			print("no es válido")
			self.context = {
								'form':form,
								'user_to_modific': user_to_modific,
								'exercise_det': exercise_det,
						
				   			}

			return render(request, self.template_name, self.context)


	def get(self, request, *args, **kwargs):
		#validacion de que sea un superusuario
		if not request.user.is_superuser:
			return redirect('admin_login:login_admin')


		try:
			exercise_det = Exercise_det.objects.get(pk=self.kwargs['pk'])
		except Exercise_det.DoesNotExist:
			messages.success(request, 'El ejercicio fue eliminado o no existe', extra_tags='alert-danger')
			return redirect('content_user:list_user')		

		try:
			user_to_modific = CustomUser.objects.get(exercise_det__id = self.kwargs['pk'])
		except CustomUser.DoesNotExist:
			messages.success(request, 'El usuario fue eliminado o no existe', extra_tags='alert-danger')
			return redirect('content_user:list_user')
		
		exercise_det.devolutions = Devolution.objects.filter(
																id_lesson_fk = None,
																returned = False,
																id_user_fk = exercise_det.id_user_fk,
																id_exercise_fk= exercise_det.id_exercise_fk,
															).count()

		exercise_det.scheduled_lessons = Lesson_det.objects.filter(reset= False, id_exercise_fk= exercise_det.id_exercise_fk, id_user_fk= exercise_det.id_user_fk).exclude( lesson_status = Lesson_det.FINISHED).count()
		exercise_det.saw_lessons = Lesson_det.objects.filter(reset= False, id_exercise_fk= exercise_det.id_exercise_fk, id_user_fk= exercise_det.id_user_fk, lesson_status = Lesson_det.FINISHED).count()
		exercise_det.enable_lessons = exercise_det.total_days - (exercise_det.saw_lessons + exercise_det.bag  + exercise_det.scheduled_lessons)
		exercise_det.save()

		form = ConfigurationUserExerciseForm(instance=exercise_det)
		

		self.context = {
							'form':form,
							'user_to_modific': user_to_modific,
							'exercise_det': exercise_det,
				   		}
		return render(request, self.template_name, self.context)

#change the user plan
class UserConfigurationChangePlanView(View):
	"""In this class i show to the admin a the exercise plans to change the old plan.
		I make a union among the plan named "ninguno" and the especific plans
		because the model "PLAN" have serveral plans of diferenet exercises
	"""
	def post(self, request, *args, **kwargs):
		
		try:
			exercise_det = Exercise_det.objects.get(pk=self.kwargs['pk'])
		except Exercise_det.DoesNotExist:
			messages.success(request, 'El ejercicio fue eliminado o no existe', extra_tags='alert-danger')
			return redirect('content_user:list_user')

		form = ConfigurationUserChangePlanForm(request.POST, instance=exercise_det)

		#en el formulario verifico que no tenga clases programadas
		if form.is_valid():
			form.save()

			exercise_det.resetter()

			# print("ES VALIDO!")
			return redirect('content_user:user_configuration_plan', pk=self.kwargs['pk'])
		else:
			print("no es válido")
			messages.success(self.request, 'El usuario todavía está en una clase de {}. No se puede reinicar el plan de un ejercicio con el usuario en la clase.'.format(exercise_det.name), extra_tags='alert-danger')
		return redirect('content_user:user_configuration_change_plan', pk=self.kwargs['pk'])


	def get(self, request, *args, **kwargs):
		#validacion de que sea un superusuario
		if not request.user.is_superuser:
			return redirect('admin_login:login_admin')

		try:
			exercise_det = Exercise_det.objects.get(pk=self.kwargs['pk'])
		except Exercise_det.DoesNotExist:
			messages.success(request, 'El ejercicio fue eliminado o no existe', extra_tags='alert-danger')
			return redirect('content_user:list_user')		

		form = ConfigurationUserChangePlanForm(instance=exercise_det)

		plan_ninguno = Plan.objects.filter(name__iexact="ninguno")
		plan_actual_exercise = Plan.objects.filter(id_exercise_fk=exercise_det.id_exercise_fk)

		#here i make the unioN
		plan_actual_exercise = plan_actual_exercise.union(plan_ninguno)

		form.fields['id_plan_fk'].queryset = plan_actual_exercise.order_by("name")
		
		try:
			user_to_modific = CustomUser.objects.get(exercise_det__id = self.kwargs['pk'])
		except CustomUser.DoesNotExist:
			messages.success(request, 'El usuario fue eliminado o no existe', extra_tags='alert-danger')
			return redirect('content_user:list_user')

		context = {		
						'form':form,
						'user_to_modific': user_to_modific,
						'exercise_det': exercise_det,						
				   }
		return render(request,'users/user_configuration/change_plan.html', context)

class UserConfigurationHistoryView(View):
	"""
		In this class i show:
		 - table with all classes that a user have already seen of specific user, this contain a date filter too.
	"""
	template_name = 'users/user_configuration/table_history.html'

	def post(self, request, *args, **kwargs):
		try:
			exercise_det = Exercise_det.objects.get(pk=self.kwargs['pk'])
		except Exercise_det.DoesNotExist:
			messages.success(request, 'El ejercicio fue eliminado o no existe', extra_tags='alert-danger')
			return redirect('content_user:list_user')		

		try:
			user_to_modific = CustomUser.objects.get(exercise_det__id = self.kwargs['pk'])
		except CustomUser.DoesNotExist:
			messages.success(request, 'El usuario fue eliminado o no existe', extra_tags='alert-danger')
			return redirect('content_user:list_user')

		form =  SearchClassesForm(request.POST)
		
		if form.is_valid():

			histories_lesson  = Lesson_det.objects.filter(	
													lesson_status = Lesson_det.FINISHED,
													id_exercise_fk=exercise_det.id_exercise_fk.id,
													id_user_fk=user_to_modific.id,
													day_lesson__range=(form.cleaned_data['since'],form.cleaned_data['until'])
												   ).order_by("-day_lesson", "-hour_lesson")

			#devoluciones del usuario
			histories_devolution = Lesson_det.objects.filter(	
													devolution__id_user_fk__id =  user_to_modific.id,
													id_exercise_fk = exercise_det.id_exercise_fk.id,
													lesson_status = Lesson_det.FINISHED,
													day_lesson__range=(form.cleaned_data['since'],form.cleaned_data['until'])
											   )

			histories_lesson = histories_lesson.union(histories_devolution).order_by("-day_lesson", "-hour_lesson")

			context = {
						'form':form,
						'user_to_modific': user_to_modific,
						'exercise_det' : exercise_det,
						'histories':histories_lesson,
				       }
			# return HttpResponse("<h1>Todo ok</h1>")
			return render(request, self.template_name, context)
		else:
			print(form.errors.as_data)
			print("something happened")

			histories_lesson  = Lesson_det.objects.filter(	
												lesson_status = Lesson_det.FINISHED,
												id_exercise_fk=exercise_det.id_exercise_fk.id,
												id_user_fk=user_to_modific.id
											   )

			#devoluciones del usuario
			histories_devolution = Lesson_det.objects.filter(	
													devolution__id_user_fk__id =  user_to_modific.id,
													id_exercise_fk = exercise_det.id_exercise_fk.id,
													lesson_status = Lesson_det.FINISHED,
											   )

			histories_lesson = histories_lesson.union(histories_devolution).order_by("-day_lesson", "-hour_lesson")

			context = {	
						'form':form,
						'user_to_modific': user_to_modific,
						'exercise_det' : exercise_det,
						'histories':histories_lesson,
				       }

		return render(request, self.template_name, context)

	def get(self, request, *args, **kwargs):
		#validacion de que sea un superusuario
		if not request.user.is_superuser:
			return redirect('admin_login:login_admin')

		try:
			exercise_det = Exercise_det.objects.get(pk=self.kwargs['pk'])
		except Exercise_det.DoesNotExist:
			messages.success(request, 'El ejercicio fue eliminado o no existe', extra_tags='alert-danger')
			return redirect('content_user:list_user')		

		try:
			user_to_modific = CustomUser.objects.get(exercise_det__id = self.kwargs['pk'])
		except CustomUser.DoesNotExist:
			messages.success(request, 'El usuario fue eliminado o no existe', extra_tags='alert-danger')
			return redirect('content_user:list_user')

		histories_lesson  = Lesson_det.objects.filter(	
												lesson_status = Lesson_det.FINISHED,
												id_exercise_fk=exercise_det.id_exercise_fk.id,
												id_user_fk=user_to_modific.id
											   )
		
		#devoluciones del usuario
		histories_devolution = Lesson_det.objects.filter(	
													devolution__id_user_fk__id =  user_to_modific.id,
													id_exercise_fk = exercise_det.id_exercise_fk.id,
													lesson_status = Lesson_det.FINISHED,
											   )

		histories_lesson = histories_lesson.union(histories_devolution).order_by("-day_lesson", "-hour_lesson")

		form =  SearchClassesForm()

		context = {
						'form':form,
						'user_to_modific': user_to_modific,
						'exercise_det' : exercise_det,
						'histories':histories_lesson,
				   }
		return render(request, self.template_name, context)


class UserConfigurationResetView(View):
	"""
		here i reset the user summary. The condition to reset is the user can't has lesson scheduled
	"""
	template_name = 'users/user_configuration/reset.html'

	def post(self, request, *args, **kwargs):
		try:
			exercise_det = Exercise_det.objects.get(pk=self.kwargs['pk'])
		except Exercise_det.DoesNotExist:
			messages.success(request, 'El ejercicio fue eliminado o no existe', extra_tags='alert-danger')
			return redirect('content_user:list_user')		

		try:
			user_to_modific = CustomUser.objects.get(exercise_det__id = self.kwargs['pk'])
		except CustomUser.DoesNotExist:
			messages.success(request, 'El usuario fue eliminado o no existe', extra_tags='alert-danger')
			return redirect('content_user:list_user')


		form = ConfigurationUserResetForm(request.POST, instance=exercise_det)

		if form.is_valid():
			form.save()
			# print(form.cleaned_data)
			# print("ES VALIDO!")
			return redirect('content_user:user_configuration_class', pk=self.kwargs['pk'])
		else:
			print("no es válido")
			context = {	
						'form':form,
						'user_to_modific': user_to_modific,
						'exercise_det': exercise_det,
				   	  }
		return render(request, self.template_name, context)

	def get(self, request, *args, **kwargs):
		#validacion de que sea un superusuario
		if not request.user.is_superuser:
			return redirect('admin_login:login_admin')
		
		try:
			exercise_det = Exercise_det.objects.get(pk=self.kwargs['pk'])
		except Exercise_det.DoesNotExist:
			messages.success(request, 'El ejercicio fue eliminado o no existe', extra_tags='alert-danger')
			return redirect('content_user:list_user')		

		try:
			user_to_modific = CustomUser.objects.get(exercise_det__id = self.kwargs['pk'])
		except CustomUser.DoesNotExist:
			messages.success(request, 'El usuario fue eliminado o no existe', extra_tags='alert-danger')
			return redirect('content_user:list_user')

		form = ConfigurationUserResetForm(instance=exercise_det)

		context = {		
						'form':form,	
						'user_to_modific': user_to_modific,
						'exercise_det': exercise_det,
				   }
		return render(request, self.template_name, context)



#------------------------------------------------------------------------------------------
#API user
#------------------------------------------------------------------------------------------
def listado(request):
	lista = serializers.serialize("json", CustomUser.objects.all(), fields=['username', 'first_name', 'last_name'])
	return HttpResponse(lista, content_type='application/json')

class UserAPI(APIView):
	serializer= CustomUserSeliazer
    #authentication_classes = [TokenAuthentication]
	#permission_classes = [IsAuthenticated]
	def get(self, request, format=None):
		lista 		= CustomUser.objects.filter(is_active=True).order_by("username")
		response  	= self.serializer(lista, many=True)
		return HttpResponse(json.dumps(response.data), content_type='application/json')