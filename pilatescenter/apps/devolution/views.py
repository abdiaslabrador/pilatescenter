from django.shortcuts import render, redirect
from django.http import HttpResponse
from apps.devolution.models import Devolution
from apps.create_user.models import CustomUser
from apps.exercise_det.models import Exercise_det
from apps.lesson_det.models import Lesson_det

from django.views import View
from django.contrib import messages

#------------------------------------------------------------------------------------------
#devolution
#------------------------------------------------------------------------------------------

#devolution decide
class DevolutionDecideView(View):
	template_name= 'devolution/devolution_decide.html'

	def get(self, request, *args, **kwargs):
		#validacion de que sea un superusuario
		if not request.user.is_superuser:
			return redirect('admin_login:login_admin')

		return render(request, self.template_name, {})

#devolution user list
class DevolutionNotReturnedUsersView(View):
	template_name= 'devolution/notreturned_users_list.html'

	def get(self, request, *args, **kwargs):
		#validacion de que sea un superusuario
		if not request.user.is_superuser:
			return redirect('admin_login:login_admin')

		devolutions = Devolution.objects.filter(	
													returned = False,
			 									).exclude(id_user_fk = None).order_by('id_user_fk__username').distinct('id_user_fk__username')

		context={	
					'devolutions':devolutions,
				}

		return render(request, self.template_name, context)


#devolution list
class NotReturnedListView(View):
	template_name= 'devolution/devolution_notreturned_list.html'

	def get(self, request, *args, **kwargs):
		#validacion de que sea un superusuario
		if not request.user.is_superuser:
			return redirect('admin_login:login_admin')

		devolutions = Devolution.objects.filter(	
													returned = False,
													id_user_fk = self.kwargs['id_user'],
			 									).order_by("id_exercise_fk__name", "day_lesson", "hour_lesson")

		context={	
					'devolutions':devolutions,
				}

		return render(request, self.template_name, context)

#devolution user list
class DevolutionReturnedUsersView(View):
	template_name= 'devolution/returned_users_list.html'

	def get(self, request, *args, **kwargs):
		#validacion de que sea un superusuario
		if not request.user.is_superuser:
			return redirect('admin_login:login_admin')

		devolutions = Devolution.objects.filter(	
													returned = True,
			 									).exclude(id_user_fk = None).order_by('id_user_fk__username').distinct('id_user_fk__username')

		context={	
					'devolutions':devolutions,
				}

		return render(request, self.template_name, context)


#devolution list
class ReturnedListView(View):
	template_name= 'devolution/devolution_returned_list.html'

	def get(self, request, *args, **kwargs):
		#validacion de que sea un superusuario
		if not request.user.is_superuser:
			return redirect('admin_login:login_admin')

		devolutions = Devolution.objects.filter(	
													returned = True,
													id_user_fk = self.kwargs['id_user']
			 									).order_by("id_exercise_fk__name", "day_lesson", "hour_lesson")

		context={	
					'devolutions':devolutions,
				}

		return render(request, self.template_name, context)

#devolution see
class DevolutionSeeView(View):
	template_name= ''
	

	def get(self, request, *args, **kwargs):
		
		#validacion de que sea un superusuario
		if not request.user.is_superuser:
			return redirect('admin_login:login_admin')

		try:
			devolution = Devolution.objects.get(id=self.kwargs['id_devolution'])
		except Devolution.DoesNotExist:
			messages.success(request, 'La devolucion que desea manipular fue eliminada o no existe', extra_tags='alert-danger')
			return redirect('devolution:decide_devolution')		

		context={	
					'devolution':devolution
				}

		return render(request, self.template_name, context)

#devolution delete
class DevolutionDeleteView(View):	
	def get(self, request, *args, **kwargs):
		#validacion de que sea un superusuario
		if not request.user.is_superuser:
			return redirect('admin_login:login_admin')

		try:
			devolution = Devolution.objects.get(id=self.kwargs['id_devolution'])
		except Devolution.DoesNotExist:
			messages.success(request, 'La devolucion que desea manipular fue eliminada o no existe', extra_tags='alert-danger')
			return redirect('devolution:decide_devolution')
			
		devolution.delete()

		return redirect('devolution:decide_devolution')

#devolution update
class UpdateDevolutionView(View):
	"""
		Este es la view que se muestra al entrar en una lección y luego querer añadir devoluciones.
		muestra los usuarios que está en la clase, que esta en la clase con devoluciones y la lista de 
		usuarios con devolciones
	"""
	template_name= 'devolution/devolution_lesson_user.html'

	def get(self, request, *args, **kwargs):
		#validacion de que sea un superusuario
		if not request.user.is_superuser:
			return redirect('admin_login:login_admin')

		try:
			lesson = Lesson_det.objects.get(id=self.kwargs['id_lesson'])
		except Lesson_det.DoesNotExist:
			messages.success(request, 'La clase que desea manipular fue eliminada o no existe', extra_tags='alert-danger')
			return redirect('lesson:list_lesson_exercise_action')
		
		#usuarios que están en la clase
		users_in_lesson = CustomUser.objects.filter(
														is_active=True, 
														lesson_det__id=lesson.id
													).order_by('username')
		#usuarios que están en devoluciones
		users_devolution = CustomUser.objects.filter(	
														is_active=True,
														devolution__id_lesson_fk__id=lesson.id,
													)

		#hago esta igualación para no afectar a los usuarios que están en la clase
		users_list = users_in_lesson

		"""
		hago la unión de los usuarios en la clase y los usuarios en las devoluciones para 
		luego hacer una exclusión

		"""
		users_list = users_list.union(users_devolution).values('id')
		
		devolutions = Devolution.objects.filter(
												id_user_fk__is_active = True,
												id_user_fk__exercise_det__reset=True,
			 									returned = False,
			 									id_lesson_fk = None,
			 									id_exercise_fk = lesson.id_exercise_fk,
			 								  ).order_by('id_user_fk__username').distinct('id_user_fk__username').exclude(id_user_fk__id__in=users_list)

		context={	
					'lesson': lesson,
					'users_in_lesson': users_in_lesson,
					'devolutions': devolutions,
					'users_devolution': users_devolution,
				}

		return render(request, self.template_name, context)

class AddToDevolutionView(View):
	"""
		en esta view se encarga de añadir la devolución de un usuario a una clase 
		en el área de las devoluciones.
		Requisitos: 
		El usuario no puede estar en la clase.
		El usuario no puede estar en las devoluciones
		El usuario tiene que tener devoluciones
	"""
	def get(self, request, *args, **kwargs):
		#validacion de que sea un superusuario
		if not request.user.is_superuser:
			return redirect('admin_login:login_admin')

		#validación de que la lección exista	
		try:
			lesson = Lesson_det.objects.get(id=self.kwargs['id_lesson'])
		except Lesson_det.DoesNotExist:
			messages.success(request, 'La clase que desea manipular fue eliminada o no existe', extra_tags='alert-danger')
			return redirect('lesson:list_lesson_exercise_action')

		#validación de que la clase no esté vista
		if lesson.lesson_status == Lesson_det.FINISHED:
			messages.success(request, 'La clase ya fue vista', extra_tags='alert-danger')
			return redirect('lesson:list_lesson_exercise_action')

		#validación de que el usuario todavía exista
		try:
			CustomUser.objects.get(id=self.kwargs['id_user'])
		except CustomUser.DoesNotExist:
			messages.success(request, 'El usuario fue eliminado', extra_tags='alert-danger')
			return redirect('devolution:update_devolution', id_lesson=self.kwargs['id_lesson'])

		"""
			obtengo la única validación que hay  aúnque la relación que hay es many to many solo hay una
			lección relacionada a la devolucíón
		"""
		devolution = Devolution.objects.filter(
												returned = False,
												id_user_fk = self.kwargs['id_user'],
												id_lesson_fk = None,
												id_exercise_fk = lesson.id_exercise_fk,
											   ).order_by("day_lesson", "hour_lesson").first()

		if devolution == None:
			messages.success(request, 'El usuario no tiene devoluciones', extra_tags='alert-danger')
			return redirect('devolution:update_devolution', id_lesson=self.kwargs['id_lesson'])

		try:
			user_exercise_det = Exercise_det.objects.get(id_exercise_fk=lesson.id_exercise_fk, id_user_fk=self.kwargs['id_user'])
		except Exercise_det.DoesNotExist:
			messages.success(request, 'El ejercicio fue eliminado o no existe', extra_tags='alert-danger')
			return redirect('lesson:list_lesson_exercise_action')

		no_in_class = Lesson_det.objects.filter(id=lesson.id, id_user_fk=self.kwargs['id_user']).count() == 0
		no_in_devolution = Devolution.objects.filter(id_lesson_fk=lesson.id, id_user_fk=self.kwargs['id_user']).count() == 0
		has_devolution = user_exercise_det.devolutions > 0

		
		if no_in_class and no_in_devolution and has_devolution:
			if lesson.cant_in < lesson.cant_max:
				devolution.id_lesson_fk.add(lesson)

		elif no_in_class == False:
			messages.success(request, 'El está en la clase', extra_tags='alert-danger')
			return redirect('devolution:update_devolution', id_lesson=self.kwargs['id_lesson'])

		elif no_in_devolution == False:
			messages.success(request, 'El está en las devoluciones', extra_tags='alert-danger')
			return redirect('devolution:update_devolution', id_lesson=self.kwargs['id_lesson'])

		elif has_devolution == False:		
			messages.success(request, 'El usuario no tiene bien el contador de devoluciones', extra_tags='alert-danger')
			return redirect('devolution:update_devolution', id_lesson=self.kwargs['id_lesson'])

		return redirect('devolution:update_devolution', id_lesson=self.kwargs['id_lesson'])


class TakeOutToDevolutionView(View):
	"""
		en esta view se encarga para sacar al usuario que está en las devoluciones de una clase 
		en el área de las devoluciones
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
			messages.success(request, 'El usuario no está', extra_tags='alert-danger')
			return redirect('devolution:update_devolution', id_lesson=self.kwargs['id_lesson'])

		devolution.id_lesson_fk.remove(lesson)

		return redirect('devolution:update_devolution', id_lesson=self.kwargs['id_lesson'])

class TakeOutToUsersLessonView(View):
	"""
		esta el la view para sacar al usuario que está en la clase en el área de las devoluciones
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
			user = CustomUser.objects.get(id=self.kwargs['id_user'])
		except CustomUser.DoesNotExist:
			messages.success(request, 'El usuario fue eliminado', extra_tags='alert-danger')
			return redirect('devolution:update_devolution', id_lesson=self.kwargs['id_lesson'])
		
		#me aseguro que el usuario esté en la clase (por seguridad) (esta query es m2m)
		if Lesson_det.objects.filter(id=lesson.id, id_user_fk=user).count() > 0:
			#me aseguro que hayan usuarios en la clase
			if lesson.id_user_fk.count() > 0:
				lesson.id_user_fk.remove(user)#saco al usuario
		else:
			messages.success(request, 'El usuario no está', extra_tags='alert-danger')
			
		return redirect('devolution:update_devolution', id_lesson=self.kwargs['id_lesson'])