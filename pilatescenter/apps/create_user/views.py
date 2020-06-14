from django.shortcuts import render, redirect
from django.http import  HttpResponse

#views
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .forms import UserCreationForm, ChangePasswordForm, UserUpdateForm
from django.views.generic.list import ListView
from django.views import View

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
from apps.exercise_det.models import Exercise_det
from .models import CustomUser

class ListUserView(ListView):
	model = CustomUser
	template_name = 'users/list_users.html'
	paginate_by = 5

	def get_queryset(self):
		queryset = CustomUser.objects.filter(is_active=True, is_visible=True).order_by("username")
		return queryset

	def get_context_data(self, **kwargs):
		context = super(ListUserView, self).get_context_data(**kwargs)
		users = self.get_queryset()
		page = self.request.GET.get('page')
		paginator = Paginator(users, self.paginate_by)

		try:
			users = paginator.page(page)
		except PageNotAnInteger:
		    users = paginator.page(1)
		except EmptyPage:
		    users = paginator.page(paginator.num_pages)
		context['users'] = users

		return context


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

			return redirect('content_user:list_user')
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
			return redirect('content_user:list_user')
		# else: #si el formuñario no esválido, esto es para pruebas
		# 	# print("NO es invalido chao!")
		# 	return render(request,'users/modific_user.html', {'form':form})
	contexto={
				'form':form,
				'exercises_list': exercises,
			 }
	return render(request,'users/modific_user.html', contexto)

class DeleteUserView(View):
	"""
		Pendiente: cuando un usuario se elimina sacarlo de todas las clases
 	"""
	def get(self, request, *args, **kwargs):
		user = CustomUser.objects.get(pk=self.kwargs['pk'])
		user.is_active=False
		user.is_visible=False
		user.save()
		return redirect('content_user:list_locked_user')

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
		context['users'] = CustomUser.objects.filter(is_active=False, is_visible=True).order_by("username")
		return context

class LockUserView(View):
	"""
		Pendiente: cuando un usuario se bloquea sacarlo de todas las clases
 	"""
	def get(self, request, *args, **kwargs):
		user = CustomUser.objects.get(pk=self.kwargs['pk'])
		user.is_active=False
		user.save()
		return redirect('content_user:list_user')

class  UnlockUserView(View):

		def get(self, request, *args, **kwargs):
			user = CustomUser.objects.get(pk=self.kwargs['pk'])
			user.is_active=True
			user.save()
			return redirect('content_user:list_locked_user')

def listado(request):
	lista = serializers.serialize("json", CustomUser.objects.all(), fields=['username', 'first_name', 'last_name'])
	return HttpResponse(lista, content_type='application/json')

class UserAPI(APIView):
	serializer= CustomUserSeliazer
#	authentication_classes = [TokenAuthentication]
	#permission_classes = [IsAuthenticated]


	def get(self, request, format=None):
		lista 		= CustomUser.objects.filter(is_active=True, is_visible=True).order_by("username")
		response  	= self.serializer(lista, many=True)
		return HttpResponse(json.dumps(response.data), content_type='application/json')
