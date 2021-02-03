from django.shortcuts import render, redirect
from django.http import HttpResponse

from apps.create_user.models import CustomUser
from apps.exercise.models import Exercise
from apps.system.models import Contact, SystemPilates
from django.views import View



class UserHomeView(View):
	template_name='user_site/home/home.html'
	context = {}

	def get(self, request, *args, **kwargs):
		if request.user.is_anonymous:
			return redirect('login:login')
		else:
			exercises = Exercise.objects.all().order_by("name")
			self.context = {
							'exercises':exercises
					  }
		
		return render(request, self.template_name, self.context)

class UserContactView(View):
	template_name='user_site/contact/contact.html'
	context = {}

	def get(self, request, *args, **kwargs):
		if request.user.is_anonymous:
			return redirect('login:login')
		else:
			contact = Contact.objects.order_by('id').first()
			if contact == None:
				contact = Contact.objects.create()
			self.context = {
							
							'contact':contact,
					  }
		
		return render(request, self.template_name, self.context)

class UserRulesView(View):
	template_name='user_site/rules/rules.html'
	context = {}

	def get(self, request, *args, **kwargs):
		if request.user.is_anonymous:
			return redirect('login:login')
		else:
			systempilates = SystemPilates.objects.order_by('id').first()
			if systempilates == None:
				systempilates = SystemPilates.objects.create()

			self.context = {
							
							'systempilates':systempilates,
					  }
		
		return render(request, self.template_name, self.context)
