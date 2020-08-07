from django.shortcuts import render, redirect
from django.http import HttpResponse

from apps.create_user.models import CustomUser
from apps.exercise_det.models import Exercise_det
from apps.lesson_det.models import Lesson_det
from django.views import View
from django.contrib import messages

from .forms import UserUpdateForm, ChangePasswordForm


class UserConfigurationProfileView(View):
	"""
		This class updates the user personal information
	"""	
	template_name='user_site/profile/configuration_profile.html'
	context = {}
	
	def post(self, request, *args, **kwargs):
		user=CustomUser.objects.get(pk=request.user.id)
		form = UserUpdateForm(request.POST, instance=user)
		if form.is_valid():
			form.save()
			# print("ES VALIDO!")
			messages.success(self.request, 'Se ha cambiado con exito los datos', extra_tags='alert-success')
			return redirect('user_profile:configuration_profile')
		else:
			self.context={
				'form':form,
				'user_to_modific':user,
			 }

	def get(self, request, *args, **kwargs):
		
		if request.user.is_anonymous:
			return redirect('user_login:user_login_form')
		else:
			
			user=CustomUser.objects.get(pk=request.user.id)
			form = UserUpdateForm(instance=user)
			self.context={
				'form':form,
				'user_to_modific':user,
			 }
		return render(request, self.template_name, self.context)



#Changing the user password
class UserChangePasswordView(View):

	def post(self, request, *args, **kwargs):
		user=CustomUser.objects.get(pk=request.user.id)
		form = ChangePasswordForm(request.POST)
		if form.is_valid():
			# print("ES VALIDO!" + " " + form.cleaned_data['password'])
			user.set_password(form.cleaned_data['password'])
			user.save()
			messages.success(self.request, 'Se ha cambiado con exito la clave', extra_tags='alert-success')
			return redirect('user_profile:configuration_profile')
		else:
			form = ChangePasswordForm()
			return render(request,'user_site/profile/change_password_user.html', {'form':form})

	def get(self, request, *args, **kwargs):
		if request.user.is_anonymous:
			return redirect('user_login:user_login_form')
			
		form = ChangePasswordForm()
		return render(request,'user_site/profile/change_password_user.html', {'form':form})
