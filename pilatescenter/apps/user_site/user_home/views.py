from django.shortcuts import render, redirect
from django.http import HttpResponse

from apps.create_user.models import CustomUser
from apps.exercise.models import Exercise
from django.views import View



class UserHomeView(View):
	template_name='user_site/home/home.html'
	context = {}

	def get(self, request, *args, **kwargs):
		if request.user.is_anonymous:
			return redirect('user_login:user_login_form')
		else:
			exercises = Exercise.objects.all().order_by("name")
			self.context = {
							'exercises':exercises
					  }
		
		return render(request, self.template_name, self.context)



