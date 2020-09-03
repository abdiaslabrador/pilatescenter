from django.shortcuts import render, redirect
from django.http import HttpResponse
from apps.devolution.models import Devolution
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
			 									)

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
			 									)

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
		in this class i pass by the post method the date selected in the form to another view by a url
	"""
	template_name= 'devolution/devolution_update.html'

	def get(self, request, *args, **kwargs):
		#validacion de que sea un superusuario
		if not request.user.is_superuser:
			return redirect('admin_login:login_admin')

		
		users_in_lesson = CustomUser.objects.filter(is_active=True, lesson_det__id=kwargs['id_lesson']).order_by('username') 
		all_users = CustomUser.objects.filter(
			 									is_active = True,
			 									exercise_det__id_exercise_fk=lesson.id_exercise_fk,
			 									exercise_det__reset=True
			 								  ).order_by('username')

		context={	
					'lesson':lesson,
					'users_in_lesson':users_in_lesson,
					'all_users': all_users,
					'form':form,
				}

