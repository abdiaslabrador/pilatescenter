from django import forms
from .models import Lesson_det
from apps.exercise.models import Hour, Exercise


#------------------------------------------------------------------------------------------
#lesson
#------------------------------------------------------------------------------------------
class CreateLessonForm(forms.Form):
	
	day_lesson = forms.DateField(label = "Día:", required=True)
	


class CreateLessonSearchForm(forms.Form):
	#I create the exercise variable to show the exercise name
	exercise = forms.CharField(label='Tipo de ejercicio',required=True, max_length=64, widget=forms.TextInput(attrs={'readonly':'readonly'}))
	day_lesson = forms.DateField(label='Ejercicio', required=True, widget=forms.TextInput(attrs={'readonly':'readonly'}))
	hour = forms.ModelChoiceField(label='Hora', required=True, queryset=Hour.objects.all())
	cant_max = forms.IntegerField(label='Cant max',required=True, min_value=0)


class SearchClassesForm(forms.Form):
	since = forms.DateField(required=True)
	until = forms.DateField(required=True)

class UpdateLessonForm(forms.ModelForm):
	day_lesson = forms.DateField(label='Fecha:', required=True, widget=forms.DateInput(format = '%Y-%m-%d',attrs={'type': 'date'}))
	hour_chance = forms.TimeField(label="Hora chance:", required=True)
	hour_lesson	= forms.TimeField(label="Hora clase:", required=True)
	hour_end = forms.TimeField(label="Hora final: ", required=True)
	cant_max = forms.IntegerField(min_value = 0, required=True)

	class Meta:
		model= Lesson_det
		fields= (
					'day_lesson',
					'hour_chance',
					'hour_lesson',
					'hour_end',
					'cant_max',
				)