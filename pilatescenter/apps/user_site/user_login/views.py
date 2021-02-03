from django.shortcuts import render, redirect
from django.http import HttpResponse

from .forms import LoginForm
from apps.create_user.models import CustomUser

from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView, LogoutView
from django.views import View



class UserLoginView(View): #class based view
	template_name='user_site/login/login.html'

	def post(self, request, *args, **kwargs):
		form = LoginForm(request.POST)
		if form.is_valid():
			#the username is coverted in lowercase in the forms.py
			user= CustomUser.objects.get(username=form.cleaned_data['username'])
			login(request, user)
			return redirect("user_home:user_home")
		else:
			print(form.errors)
		return render(request, self.template_name, {'form':form})

	def get(self, request, *args, **kwargs):
		form = LoginForm()
		return render(request, self.template_name, {'form':form})


class UserLogoutView(View):
	
	def get(self, request, *args, **kwargs):
		logout(request)
		return redirect('login:login')
