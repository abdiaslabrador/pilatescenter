
from django.shortcuts import render, redirect
from django.http import  HttpResponse

#views
from .forms import ( 
						UserCreationForm, ChangePasswordForm,
						 UserUpdateForm, SearchClasses
					)

from apps.exercise_det.forms import ( 
									  ConfigurationUserExerciseForm, ConfigurationUserChangePlanForm,
									  ConfigurationUserResetForm
									)
from django.views.generic.list import ListView
from django.views import View
from django.contrib import messages


#django rest-rest_framework
from django.core import serializers
from .serializers import CustomUserSeliazer
from rest_framework.serializers import  ModelSerializer
import json
from rest_framework.views import  APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication


#this is necesary to make the relations between Exercise_det and customuser
from apps.plan.models import Plan
from apps.exercise.models import Exercise
from apps.exercise_det.models import Exercise_det, update_resumen
from apps.lesson_det.models import Lesson_det
from apps.history_det.models import History_det
from .models import CustomUser


#------------------------------------------------------------------------------------------
#user
#------------------------------------------------------------------------------------------
class ListUserView(ListView):
	model = CustomUser
	template_name = 'users/list_users.html'


	def get_queryset(self):
		queryset = CustomUser.objects.filter(is_active=True).order_by("username")
		return queryset

	def get_context_data(self, **kwargs):
		context = super(ListUserView, self).get_context_data(**kwargs)
		users = self.get_queryset()
		context['users'] = users
		return context


#Creating a user
def create_user(request):
	if request.method == 'POST':
		form = UserCreationForm(request.POST)
		if form.is_valid():
			form.save()
			print("ES VALIDO!")

			"""#This not work if i create a user in the admin page, it means, y i create a user
			#in the admin page, the user won't have the relation between users and exercise_det
			exercises=Exercise.objects.all()
			if exercises.count() > 0:
				form.save()
				user=CustomUser.objects.get(username=form.cleaned_data['username'])
				plan=Plan.objects.get(name__icontains="ninguno")

				x = None
				for i in exercises:
					Exercise_det.objects.create(name=i.name, id_plan_fk=plan, id_exercise_fk=i, id_user_fk=user)
			else:
				print("\n No hay ejercicios creados. No se le asignò ejercicios a este usuario.")"""

			return redirect('content_user:list_user')
		else:
			print("es invalido chao!")
	else:

		form = UserCreationForm()

	return render(request,'users/create_user.html', {'form':form})

#Updating a user
def modific_user(request, pk):


	user=CustomUser.objects.get(pk=pk)
	exercises_det = Exercise_det.objects.filter(id_user_fk = user).order_by('name')
	if request.method == 'GET':
		form = UserUpdateForm(instance=user, initial={'primarykey': user.pk})
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

class DeleteUserView(View):
	"""
		Pendiente: cuando un usuario se elimina sacarlo de todas las clases
 	"""
	def get(self, request, *args, **kwargs):


		user = CustomUser.objects.get(pk=self.kwargs['pk'])

		if Lesson_det.objects.filter(id_user_fk= user, saw=False).count() > 0:
			messages.success(self.request, 'No se puede eliminar un usuario con clases programadas', extra_tags='alert-danger')
			return redirect('content_user:list_user')

		user.delete()
		return redirect('content_user:list_user')

#Changing the user password
def change_password_user(request, pk):

	user=CustomUser.objects.get(pk=pk)
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
		form = ChangePasswordForm()
	return render(request,'users/change_password_user.html', {'form':form})


class ListLockedUserView(ListView):

	model = CustomUser
	template_name = 'users/locked_users.html'


	def get_context_data(self, **kwargs):
		context = super(ListLockedUserView, self).get_context_data(**kwargs)
		context['users'] = CustomUser.objects.filter(is_active=False).order_by("username")
		return context

class LockUserView(View):
	"""
		Pendiente: cuando un usuario se bloquea sacarlo de todas las clases
 	"""
	def get(self, request, *args, **kwargs):
		user = CustomUser.objects.get(pk=self.kwargs['pk'])

		if Lesson_det.objects.filter(id_user_fk= user, saw=False).count() > 0:
			messages.success(self.request, 'No se puede bloquear un usuario con clases programadas', extra_tags='alert-danger')
			return redirect('content_user:list_user')

		user.is_active=False
		user.save()
		return redirect('content_user:list_user')

class  UnlockUserView(View):

	def get(self, request, *args, **kwargs):
		user = CustomUser.objects.get(pk=self.kwargs['pk'])
		user.is_active=True
		user.save()
		return redirect('content_user:list_locked_user')



class ResetUsersView(View):
	def get(self, request, *args, **kwargs):

		exercise = Exercise.objects.get(pk=self.kwargs['pk'])
				
		#esto es para verificar que no hayan usuarios con clases programadas para hacer el reinicio
		lessons = Lesson_det.objects.filter(saw=False, id_exercise_fk=exercise).order_by("day_lesson")
		for lesson in lessons:
			if lesson.id_user_fk.all().count() > 0: #obtengo todos los usurios de la clase y pregunto is es mayor a 0
				messages.success(self.request, 'Hay almenos una clase con usuarios dentro. No se puede reinicar un ejercicio con usuarios en clases', extra_tags='alert-danger')
				return redirect('exercise:list_exercise')

		#obtengo todos los exercise_det de los usuarios con el respectivo ejercicio que se puedan reiniciar
		exercises_det = Exercise_det.objects.filter(id_exercise_fk=exercise).filter(reset=True)


		for exercise_det in exercises_det:
			exercise_det.resetter()


		messages.success(self.request, 'Se han reiniciado los usuarios', extra_tags='alert-success')
		return redirect('exercise:list_exercise')

#------------------------------------------------------------------------------------------
#setting up the user
#------------------------------------------------------------------------------------------
class UserConfigurationClassView(View):
	template_name= 'users/user_configuration/table_lesson.html'

	def post(self, request, *args, **kwargs):
		exercise_det=Exercise_det.objects.get(id = self.kwargs['pk'])
		user_to_modific = CustomUser.objects.get(exercise_det__id = self.kwargs['pk'])
		form =  SearchClasses(request.POST)

		if form.is_valid():
			
			lessons = Lesson_det.objects.filter(
													saw=False,
													day_lesson__range=(form.cleaned_data['since'],form.cleaned_data['until']),
												    id_exercise_fk=exercise_det.id_exercise_fk.id,
												    id_user_fk=user_to_modific.id
												    

												).order_by("day_lesson")	
			context = {
						'exercise_det' : exercise_det,
						'user_to_modific': user_to_modific,
						'lessons':lessons,
						'form':form
				       }
			# return HttpResponse("<h1>Todo ok</h1>")
			return render(request, self.template_name, context)
		else:
			print(form.errors.as_data)
			print("something happened")

			lessons = Lesson_det.objects.filter(saw= False, id_exercise_fk=exercise_det.id_exercise_fk.id, id_user_fk=user_to_modific.id)
			context = {
						'exercise_det' : exercise_det,
						'user_to_modific': user_to_modific,
						'lessons':lessons,
						'form':form
				       }
		return render(request, self.template_name, context)

	def get(self, request, *args, **kwargs):
		form = SearchClasses()
		exercise_det 	= Exercise_det.objects.get(pk=self.kwargs['pk'])
		user_to_modific = CustomUser.objects.get(exercise_det__id = self.kwargs['pk'])
		lessons = Lesson_det.objects.filter(saw= False, id_exercise_fk=exercise_det.id_exercise_fk.id, id_user_fk=user_to_modific.id)

		context = {	
						
						'exercise_det' : exercise_det,
						'user_to_modific': user_to_modific,
						'form':form,
						'lessons':lessons,
				   }
		return render(request, self.template_name, context)

class UserConfigurationSawLessonView(View):

	def get(self, request, *args, **kwargs):
		try:
			lesson = Lesson_det.objects.get(id=self.kwargs['id_lesson'])
		except Lesson_det.DoesNotExist:
			messages.success(request, 'La clase que desea manipular fue eliminada o no existe', extra_tags='alert-danger')
			return redirect('content_user:user_configuration_class', pk=self.kwargs['id_exercise_det'])

		if lesson.saw == True:
			messages.success(request, 'La clase ya fue vista', extra_tags='alert-danger')
			return redirect('content_user:user_configuration_class', pk=self.kwargs['id_exercise_det'])
		
		
		lesson.saw = True
		lesson.save()
		update_resumen(lesson)

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

		return redirect('content_user:user_configuration_class', pk=self.kwargs['id_exercise_det'])
		
class DeleteLessonView(View):
	def get(self, request, *args, **kwargs):
		try:
			lesson = Lesson_det.objects.get(id=self.kwargs['id_lesson'])
		except Lesson_det.DoesNotExist:
			messages.success(request, 'La clase que desea manipular fue eliminada o no existe', extra_tags='alert-danger')
			return redirect('content_user:user_configuration_class', pk=self.kwargs['id_exercise_det'])	

		if lesson.saw == True:
			messages.success(request, 'La clase ya fue vista', extra_tags='alert-danger')
			return redirect('content_user:user_configuration_class', pk=self.kwargs['id_exercise_det'])	
			
		users_in_lesson = lesson.id_user_fk.all() #i get all users that are in the lesson		

		for user in users_in_lesson:
			user_exercise_det = Exercise_det.objects.get(id_exercise_fk= lesson.id_exercise_fk, id_user_fk= user)

			#Esta el la cantidad de clases programadas del usuario
			cant_lesson_scheduled = Lesson_det.objects.filter(saw= False, id_exercise_fk= lesson.id_exercise_fk, id_user_fk= user).exclude(id=lesson.id).count()#here rest to each one in the class -1 before clear the class
			user_exercise_det.scheduled_lessons = cant_lesson_scheduled
			user_exercise_det.enable_lessons = user_exercise_det.total_days - (user_exercise_det.saw_lessons + user_exercise_det.bag  + user_exercise_det.scheduled_lessons)
			user_exercise_det.save()

		lesson.delete()

		return redirect('content_user:user_configuration_class', pk=self.kwargs['id_exercise_det'])	

class UserConfigurationPlanView(View):
	template_name = 'users/user_configuration/resumen.html'
	context = {}

	def post(self, request, *args, **kwargs):
		exercise_det= Exercise_det.objects.get(id=self.kwargs['pk'])
		form = ConfigurationUserExerciseForm(request.POST, instance=exercise_det)
		user_to_modific = CustomUser.objects.get(exercise_det__id = self.kwargs['pk'])

		#this "if" is part of a validation of reset condition of the user
		if exercise_det.reset == True:
			if form.is_valid():
				form.save()
				# print("Este es la data" + str(form.cleaned_data))
				# print("ES VALIDO!")
				return redirect('content_user:user_configuration_class', pk=self.kwargs['pk'])
			else:
				print("no es válido")
				self.context = {
							'user_to_modific': user_to_modific,
							'exercise_det': exercise_det,
							'form':form
					   }
			return render(request, self.template_name, self.context)

		elif exercise_det.reset == False: #esto es por si intenta modificar un usuario que ya ha fue previamente colocado en modo "No reiniciar"
			messages.success(self.request, 'No se han guardado cambios porque previamente ha activado la opción de "No reiniciar"', extra_tags='alert-danger')
			print("no es válido")
			self.context = {
						'user_to_modific': user_to_modific,
						'exercise_det': exercise_det,
						'form':form
				   }

			return render(request, self.template_name, self.context)


	def get(self, request, *args, **kwargs):
		exercise_det 	= Exercise_det.objects.get(pk=self.kwargs['pk'])
		form 			= ConfigurationUserExerciseForm(instance=exercise_det)
		user_to_modific = CustomUser.objects.get(exercise_det__id = self.kwargs['pk'])

		self.context = {
						'user_to_modific': user_to_modific,
						'exercise_det': exercise_det,
						'form':form
				   }
		return render(request, self.template_name, self.context)

class UserConfigurationChangePlanView(View):

	def post(self, request, *args, **kwargs):
		
		exercise_det= Exercise_det.objects.get(id=self.kwargs['pk'])
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
		exercise_det = Exercise_det.objects.get(pk=self.kwargs['pk'])
		form = ConfigurationUserChangePlanForm(instance=exercise_det)

		plan_ninguno = Plan.objects.filter(name__iexact="ninguno")
		plan_actual_exercise = Plan.objects.filter(id_exercise_fk__name__iexact=exercise_det.name)
		plan_actual_exercise = plan_actual_exercise.union(plan_ninguno)

		form.fields['id_plan_fk'].queryset = plan_actual_exercise.order_by("name")
		user_to_modific = CustomUser.objects.get(exercise_det__id = self.kwargs['pk'])

		context = {
						'user_to_modific': user_to_modific,
						'exercise_det': exercise_det,
						'form':form
				   }
		return render(request,'users/user_configuration/change_plan.html', context)

class UserConfigurationHistoryView(View):
	template_name = 'users/user_configuration/table_history.html'

	def post(self, request, *args, **kwargs):
		exercise_det 	= Exercise_det.objects.get(pk=self.kwargs['pk'])
		user_to_modific = CustomUser.objects.get(exercise_det__id = self.kwargs['pk'])
		form =  SearchClasses(request.POST)
		
		if form.is_valid():
			
			histories = History_det.objects.filter( 
														id_exercise_fk=exercise_det.id_exercise_fk.id, 
														id_user_fk=user_to_modific.id,
														day_lesson__range=(form.cleaned_data['since'],form.cleaned_data['until'])

													).order_by("day_lesson")

			context = {
						'user_to_modific': user_to_modific,
						'exercise_det' : exercise_det,
						'histories':histories,
						'form':form
				       }
			# return HttpResponse("<h1>Todo ok</h1>")
			return render(request, self.template_name, context)
		else:
			print(form.errors.as_data)
			print("something happened")
			histories = History_det.objects.filter(id_exercise_fk=exercise_det.id_exercise_fk.id, id_user_fk=user_to_modific.id).order_by("day_lesson")

			context = {
						'user_to_modific': user_to_modific,
						'exercise_det' : exercise_det,
						'histories':histories,
						'form':form
				       }
		return render(request, self.template_name, context)

	def get(self, request, *args, **kwargs):
		exercise_det 	= Exercise_det.objects.get(pk=self.kwargs['pk'])
		user_to_modific = CustomUser.objects.get(exercise_det__id = self.kwargs['pk'])
		histories = History_det.objects.filter(id_exercise_fk=exercise_det.id_exercise_fk.id, id_user_fk=user_to_modific.id).order_by("day_lesson")
		# lessons = Lesson_det.objects.filter(saw= True, id_exercise_fk=exercise_det.id_exercise_fk.id, id_user_fk=user_to_modific.id)
		form =  SearchClasses()

		context = {
						'user_to_modific': user_to_modific,
						'exercise_det' : exercise_det,
						'histories':histories,
						'form':form
				   }
		return render(request, self.template_name, context)

class UserConfigurationResetView(View):
	template_name = 'users/user_configuration/reset.html'

	def post(self, request, *args, **kwargs):
		exercise_det= Exercise_det.objects.get(id=self.kwargs['pk'])
		user_to_modific = CustomUser.objects.get(exercise_det__id = self.kwargs['pk'])
		form = ConfigurationUserResetForm(request.POST, instance=exercise_det)

		if form.is_valid():
			form.save()
			# print(form.cleaned_data)
			# print("ES VALIDO!")
			return redirect('content_user:user_configuration_class', pk=self.kwargs['pk'])
		else:
			print("no es válido")
			context = {
						'user_to_modific': user_to_modific,
						'exercise_det': exercise_det,
						'form':form
				   }
		return render(request, self.template_name, context)

	def get(self, request, *args, **kwargs):
		exercise_det 	= Exercise_det.objects.get(pk=self.kwargs['pk'])
		user_to_modific = CustomUser.objects.get(exercise_det__id = self.kwargs['pk'])
		form = ConfigurationUserResetForm(instance=exercise_det)

		context = {
						'user_to_modific': user_to_modific,
						'exercise_det': exercise_det,
						'form':form
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
