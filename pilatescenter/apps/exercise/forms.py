from django import forms
from .models import Exercise
from django.core.exceptions import ValidationError
from .models import Hour, Day


#------------------------------------------------------------------------------------------
#exercise
#------------------------------------------------------------------------------------------
class CreateExerciseForm(forms.ModelForm):

	class Meta:
		model= Exercise
		fields= (
					"name",
					"description"
				)

	def clean(self):
		cleaned_data =super(CreateExerciseForm, self).clean()

	
	def clean_name(self):
		name = self.cleaned_data.get("name")

		# I compare the name with the other names of the exercises, so as not to repeat them
		if name == None or len(name) == 0:
			raise forms.ValidationError("Escriba un nombre para el ejercicio")
		print("this is the space: " + name)
		name = name.upper()

		try:
			exercise=Exercise.objects.get(name__iexact=name)
		except Exercise.DoesNotExist:
			return name

		raise forms.ValidationError("El nombre del ejercicio ya existe")





class UpdateExerciseForm(forms.ModelForm):
	primarykey = forms.IntegerField(widget=forms.HiddenInput())
	class Meta:
		model= Exercise
		fields= (
					"name",
					"description"
				)

	def clean(self):
		#here we have the username and the id
		clean = super().clean()
		name 	= self.cleaned_data.get("name")
		primarykey 	= self.cleaned_data.get("primarykey")

		if name is None or len(name) == 0:
			raise forms.ValidationError("Escriba un nombre para el ejercicio")

		name = name.upper()

		#this part compare if the name written is the same that was already
		exercise = Exercise.objects.get(pk=primarykey)
		if name == exercise.name.upper():
			self.cleaned_data['name']=name
			return clean

		#if it wasn't i compare the name with other usernames
		exercises = Exercise.objects.exclude(pk=primarykey)

		for exercise in exercises:
			if name == exercise.name.upper():
				raise forms.ValidationError("Ya este nombre lo posee otro ejercicio")

		self.cleaned_data['name']=name
		return clean



#------------------------------------------------------------------------------------------
#day
#------------------------------------------------------------------------------------------
class CreateDayForm(forms.ModelForm):
	hour_chance = forms.TimeField(label="Hora de chance", widget=forms.TextInput(attrs={'placeholder': 'formato: 02:03:AM o PM'}))
	hour_lesson = forms.TimeField(label="Hora de la clase", widget=forms.TextInput(attrs={'placeholder': 'formato: 02:03:AM o PM'}))
	hour_end = forms.TimeField(label="Hora de finalización de la clase", widget=forms.TextInput(attrs={'placeholder': 'formato: 02:03:AM o PM'}))
	id_day_fk	= forms.ModelChoiceField(queryset=Day.objects.all().order_by('name'), label= 'Día')
	class Meta:
		model = Hour
		fields = (	
					'id_day_fk',
					'hour_chance', 
					'hour_lesson', 
					'hour_end',
				)

#------------------------------------------------------------------------------------------
#hour
#------------------------------------------------------------------------------------------

class Create_hour(forms.ModelForm):
	hour_chance = forms.TimeField(label="Hora de chance", widget=forms.TextInput(attrs={'placeholder': 'formato: 02:03:AM o PM'}))
	hour_lesson = forms.TimeField(label="Hora de la clase", widget=forms.TextInput(attrs={'placeholder': 'formato: 02:03:AM o PM'}))
	hour_end = forms.TimeField(label="Hora de finalización de la clase", widget=forms.TextInput(attrs={'placeholder': 'formato: 02:03:AM o PM'}))

	class Meta:
		model = Hour
		fields = (
					'hour_chance', 
					'hour_lesson', 
					'hour_end',
				)

class UpdateHourForm(forms.ModelForm):
	primarykey = forms.IntegerField(widget=forms.HiddenInput())
	
	
	class Meta:
		model= Hour
		fields= (
					'hour_chance', 
					'hour_lesson', 
					'hour_end',
				)