from django.shortcuts import render, redirect
from django.http import HttpResponse

from apps.create_user.models import CustomUser
from apps.lesson_det.models import Lesson_det
from apps.exercise_det.models import Exercise_det
from django.views import View
from .forms import SearchLessonForm
from django.contrib import messages
from datetime import datetime ,timedelta
from django.db.models import F



class UserLessonListView(View):
	"""
		This class shows the class that a user hasn't seen yet.
	"""
	template_name='user_site/lesson_list/lesson_list.html'
	context = {}
	exercise_det = None

	def get(self, request, *args, **kwargs):
		if request.user.is_anonymous:
			return redirect('user_login:user_login_form')
		else:
			
			try:
				self.exercise_det = Exercise_det.objects.get(
															id_user_fk=request.user,
														    id_exercise_fk=self.kwargs['id_exercise']
														)
			except Exercise_det.DoesNotExist:
				messages.success(self.request, 'El ejercicio fue eliminado', extra_tags='alert-danger')
				return redirect('user_home:user_home')

			lessons = Lesson_det.objects.filter(	
													reset = False,
													id_user_fk=request.user,
													id_exercise_fk=self.kwargs['id_exercise'],
												).exclude(lesson_status = Lesson_det.FINISHED).order_by("day_lesson")
			self.context ={
							'lessons':lessons,
							'exercise_det':self.exercise_det,
					  	   }

		return render(request, self.template_name, self.context)

class UserResumenView(View):
	"""
		This shows the resumen of the users
	"""
	template_name='user_site/lesson_list/resumen/resumen.html'
	context = {}
	exercise_det = None

	def get(self, request, *args, **kwargs):
		if request.user.is_anonymous:
			return redirect('user_login:user_login_form')
		else:
			
			try:
				self.exercise_det = Exercise_det.objects.get(id=self.kwargs['id_exercise_det'])
			except Exercise_det.DoesNotExist:
				messages.success(self.request, 'El ejercicio fue eliminado', extra_tags='alert-danger')
				return redirect('user_home:user_home')

			self.context ={
							'exercise_det':self.exercise_det,
					  }
		return render(request, self.template_name, self.context)

class UserInBagView(View):
	"""
		this class puts a lesson in the user reserved lessons.
		Restriction: to do this the user must have oportunities to reserve lessons
	"""
	context = {}
	exercise_det = None

	def get(self, request, *args, **kwargs):
		if request.user.is_anonymous:
			return redirect('user_login:user_login_form')
		else:
			try:
				self.exercise_det = Exercise_det.objects.get(id=self.kwargs['id_exercise_det'])
			except Exercise_det.DoesNotExist:
				messages.success(self.request, 'El ejercicio fue eliminado', extra_tags='alert-danger')
				return redirect('user_home:user_home')

			if self.exercise_det.oportunities > 0:
				self.exercise_det.oportunities-=1				
				self.exercise_det.bag+=1
				self.exercise_det.save()
				lesson = Lesson_det.objects.get(id=self.kwargs['id_lesson'])
				lesson.id_user_fk.remove(request.user)
			else:
				messages.success(self.request, 'No tienes oportunidades para reprogramar', extra_tags='alert-danger')
			return redirect('user_lesson:lesson_list', id_exercise=self.exercise_det.id_exercise_fk.id)	
		

class UserBagView(View):
	"""
		Aquí hago unos filtros para obtener las clases donde el usuario no está y tampoco esté 
		llena, y que estas clases estén a unos ciertos días hacia adelante.
	"""
	template_name='user_site/lesson_list/bag/bag.html'
	context = {}
	exercise_det = None

	def get(self, request, *args, **kwargs):
		if request.user.is_anonymous:
			return redirect('user_login:user_login_form')
		else:
			today = datetime.today()
			
			today_delta = timedelta(days = 5)
			plus_days = today + today_delta

			try:
				self.exercise_det = Exercise_det.objects.get(id=self.kwargs['id_exercise_det'])
			except Exercise_det.DoesNotExist:
				messages.success(self.request, 'El ejercicio fue eliminado', extra_tags='alert-danger')
				return redirect('user_home:user_home')

			if self.exercise_det.bag > 0:

				days_already_have = Lesson_det.objects.filter(	
																reset=False,
																id_user_fk=request.user.id,
															).exclude(lesson_status = Lesson_det.FINISHED).values('day_lesson')

				user_days_already_have=[]
				for day in days_already_have:
					user_days_already_have.append(day['day_lesson'].strftime("%A"))
				
				
				unfiltered_lessons = Lesson_det.objects.filter(
																reset=False,
																id_exercise_fk=self.exercise_det.id_exercise_fk,
																lesson_status = Lesson_det.ENABLE,
																cant_in__lt=F('cant_max'),
																day_lesson__range=(today, plus_days),
															).exclude(cant_in=0).exclude(id_user_fk__id=request.user.id).order_by("day_lesson") 
				lessons = []
				for unfiltered_lesson in unfiltered_lessons:
					if unfiltered_lesson.day_lesson.strftime("%A") not in user_days_already_have:
						lessons.append(unfiltered_lesson)

				
				self.context ={
								'lessons':lessons,
							   }

				return render(request, self.template_name, self.context)
			else:
				messages.success(self.request, 'No tiene clases en reserva', extra_tags='alert-danger')
				return redirect('user_lesson:lesson_list', id_exercise=self.exercise_det.id_exercise_fk.id)


class UserBagDaySelectedView(View):
	"""
		this class reserves a lesson when the user presses the button "Reservar"
	"""
	context = {}

	def get(self, request, *args, **kwargs):
		if request.user.is_anonymous:
			return redirect('user_login:user_login_form')
		else:

			user = CustomUser.objects.get(id=request.user.id)
			lesson= None
			#validacion de que la lección exista			
			try:
				lesson = Lesson_det.objects.get(id=self.kwargs['id_lesson'])
			except Lesson_det.DoesNotExist:
				messages.success(self.request, 'La lección ha sido eliminada', extra_tags='alert-danger')
				return redirect('user_home:user_home')

			#validacion de que la clase todavía se pueda ver
			if lesson.cant_in == lesson.cant_max or lesson.lesson_status == Lesson_det.FINISHED:
				messages.success(self.request, 'La lección ya fu vista o ya está llena', extra_tags='alert-warning')
				return redirect('user_lesson:lesson_list', id_exercise= lesson.id_exercise_fk.id)

			exercise_det = Exercise_det.objects.get(
														id_user_fk=request.user,
														id_exercise_fk=lesson.id_exercise_fk,
													)

			if exercise_det.bag > 0:
				exercise_det.bag-=1
				exercise_det.save()
				lesson.id_user_fk.add(user)

				messages.success(self.request, 'Has agregado con exito la clase', extra_tags='alert-success')

				return redirect('user_lesson:lesson_list', id_exercise=lesson.id_exercise_fk.id)
			else:
				messages.success(self.request, 'No tiene clases en reserva', extra_tags='alert-danger')
				return redirect('user_lesson:lesson_list', id_exercise=lesson.id_exercise_fk.id)


# class UserBagSearchView(View):
# 	"""
# 		this class gives a form to the user for later looks lessons asociated for date selected. 
# 		Remember: I need to change this
# 	"""
# 	template_name='user_site/lesson_list/bag/search_lesson.html'
# 	context = {}

# 	def post(self, request, *args, **kwargs):
# 		form =  SearchLessonForm(request.POST)
# 		if form.is_valid():
# 			day=form.cleaned_data['day']
# 			day.name = day.name.lower()
# 			return redirect('user_lesson:bag', name_day=day.name, id_exercise_det=self.kwargs['id_exercise_det'])
# 		else:
# 			print(form.errors.as_data)
# 			print("something happened")
# 		return render(request, self.template_name, {'form':form})

# 	def get(self, request, *args, **kwargs):
# 		if request.user.is_anonymous:
# 			return redirect('user_login:user_login_form')
# 		else:
# 			exercise_det = Exercise_det.objects.get(id=self.kwargs['id_exercise_det'])
# 			if exercise_det.bag > 0:
# 				form = SearchLessonForm()
# 				exercise_det = self.kwargs['id_exercise_det']
# 				self.context ={
# 							'form':form,
# 					  	  }
# 				return render(request, self.template_name, self.context)
# 			else:
# 				messages.success(self.request, 'No tiene clases en reserva', extra_tags='alert-danger')
# 				return redirect('user_lesson:lesson_list', id_exercise=exercise_det.id_exercise_fk.id)
			
		

# class UserBagView(View):
# 	"""
# 		i obtain the day for the date passed by the url. I make a translate, from spanish days to  english  days for later can make a filter 
# 		and show to the user the enable dates in that day.
# 	"""
# 	template_name='user_site/lesson_list/bag/bag.html'
# 	context = {}

# 	def get(self, request, *args, **kwargs):
# 		if request.user.is_anonymous:
# 			return redirect('user_login:user_login_form')
# 		else:
# 			exercise_det = Exercise_det.objects.get(id=self.kwargs['id_exercise_det'])
# 			if exercise_det.bag > 0:
# 				week_days = {"domingo":"Sunday", "lunes":"Monday", "martes":"Tuesday", "miercoles":"Wednesday", "jueves":"Thursday", "viernes":"Friday", "sabado":"Saturday"}
# 				translate_spanish_to_english= week_days[self.kwargs['name_day']]
# 				lessons = []
# 				exercise_det = Exercise_det.objects.get(id=self.kwargs['id_exercise_det'])

# 				lessons_to_analize = Lesson_det.objects.filter(
# 														saw = False, 
# 														id_exercise_fk=exercise_det.id_exercise_fk,
# 														cant_in__lt=F('cant_max'),
# 													).exclude(id_user_fk__id=request.user.id).order_by("day_lesson")
# 				for lesson in lessons_to_analize:
# 					if translate_spanish_to_english == lesson.day_lesson.strftime("%A"):
# 						lessons.append(lesson)

				
# 				self.context ={
# 								'lessons':lessons,
# 							   }

# 				return render(request, self.template_name, self.context)
# 			else:
# 				messages.success(self.request, 'No tiene clases en reserva', extra_tags='alert-danger')
# 				return redirect('user_lesson:lesson_list', id_exercise=exercise_det.id_exercise_fk.id)