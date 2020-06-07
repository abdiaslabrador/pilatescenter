from django.shortcuts import render, redirect
from django.http import  HttpResponse

from .forms import UserCreationForm, ChangePasswordForm, UserUpdateForm
from django.views import View

from django.core import serializers
from .serializers import CustomUserSeliazer
from rest_framework.serializers import  ModelSerializer
from rest_framework.views import  APIView
import json

#this is necesary to make the relations between Exercise_det and customuser
from apps.plan.models import Plan
from apps.exercise.models import Exercise
from apps.exercise_det.models import Exercise_det
from .models import CustomUser



#Creating a user
def create_user(request):
	if request.method == 'POST':
		form = UserCreationForm(request.POST)
		if form.is_valid():
			print("ES VALIDO!")

			#This not work if i create a user in the admin page, it means, y i create a user
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
				print("\n No hay ejercicios creados. No se le asignò ejercicios a este usuario.")

			return redirect('login')
		else:
			print("es invalido chao!")
	else:

		form = UserCreationForm()

	return render(request,'users/create_user.html', {'form':form})

#Updating a user
def modific_user(request, pk):

	exercises = Exercise.objects.all()
	user=CustomUser.objects.get(pk=pk)
	if request.method == 'GET':
		form = UserUpdateForm(instance=user, initial={'primarykey': user.pk})
	else:
		form = UserUpdateForm(request.POST, instance=user)
		if form.is_valid():
			form.save()
			# print("ES VALIDO!")
			return redirect('login')
		# else: #si el formuñario no esválido, esto es para pruebas
		# 	# print("NO es invalido chao!")
		# 	return render(request,'users/modific_user.html', {'form':form})
	contexto={
				'form':form,
				'exercises_list': exercises,
			 }
	return render(request,'users/modific_user.html', contexto)


#Changing the user password
def change_password_user(request, pk):

	user=CustomUser.objects.get(pk=pk)
	if request.method == 'POST':
		form = ChangePasswordForm(request.POST)
		if form.is_valid():
			# print("ES VALIDO!" + " " + form.cleaned_data['password'])
			user.set_password(form.cleaned_data['password'])
			user.save()
			return redirect('login:login')
		# else:
			# print("NO es invalido chao!")
	else:
		form = ChangePasswordForm()
	return render(request,'users/change_password_user.html', {'form':form})

def listado(request):
	lista = serializers.serialize("json", CustomUser.objects.all(), fields=['username', 'first_name', 'last_name'])
	return HttpResponse(lista, content_type='application/json')

class UserAPI(APIView):
	serializer= CustomUserSeliazer

	def get(self, request, format=None):
		lista 		= CustomUser.objects.all()
		response  	= self.serializer(lista, many=True)
		return HttpResponse(json.dumps(response.data), content_type='application/json')
