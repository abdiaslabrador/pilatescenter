from django.shortcuts import render, redirect
from django.http import HttpResponse
from apps.devolution.models import Devolution
from apps.create_user.models import CustomUser
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
	template_name= 'devolution/devolution_notreturned_table.html'

	def get(self, request, *args, **kwargs):
		#validacion de que sea un superusuario
		if not request.user.is_superuser:
			return redirect('admin_login:login_admin')

		devolutions = Devolution.objects.filter(	
													returned = False,
													id_user_fk = self.kwargs['id_user']
			 									).order_by("day_lesson", "hour_lesson")

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
	template_name= 'devolution/devolution_returned_table.html'

	def get(self, request, *args, **kwargs):
		#validacion de que sea un superusuario
		if not request.user.is_superuser:
			return redirect('admin_login:login_admin')

		devolutions = Devolution.objects.filter(	
													returned = True,
													id_user_fk = self.kwargs['id_user']
			 									).order_by("day_lesson", "hour_lesson")

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
			return redirect('devolution:devolution_users_list')
			
		lesson_retorned=devolution.id_lesson_fk.all()[0]

		context={	
					'devolution':devolution,
					'lesson_retorned':lesson_retorned,
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
			return redirect('devolution:devolution_users_list')
			
		devolution.delete()

		return redirect('devolution:decide_devolution')

#devolution update
class UpdateDevolutionView(View):
	"""
		
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
														devolution__id_lesson_fk__id=lesson.id
													)

		#hago esta igualación para no afectar a los usuarios que están en la clase
		users_list = users_in_lesson

		"""
		hago la unión de los usuarios en la clase y los usuarios en las devoluciones para 
		luego hacer una exclusión

		"""
		users_list = users_list.union(users_devolution).values('id')
		
		all_users = CustomUser.objects.filter(
			 									is_active = True,
			 									exercise_det__id_exercise_fk=lesson.id_exercise_fk,
			 									exercise_det__reset=True,
			 									devolution__id_lesson_fk = None,
			 									devolution__returned = False,
			 								  ).order_by('username').distinct('username').exclude(id__in=users_list)

		context={	
					'lesson': lesson,
					'users_in_lesson': users_in_lesson,
					'all_users': all_users,
					'users_devolution': users_devolution,
				}

		return render(request, self.template_name, context)

class AddToDevolutionView(View):
	"""
		
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
												id_lesson_fk = None
											   ).order_by("day_lesson", "hour_lesson").first()

		if devolution == None:
			messages.success(request, 'El usuario no tiene devoluciones', extra_tags='alert-danger')
			return redirect('devolution:update_devolution', id_lesson=self.kwargs['id_lesson'])

		if lesson.cant_in < lesson.cant_max:
			devolution.id_lesson_fk.add(lesson)

		return redirect('devolution:update_devolution', id_lesson=self.kwargs['id_lesson'])


class TakeOutToDevolutionView(View):
	"""
		
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
