from django import forms
from .models import Hour
from apps.exercise.models import Exercise

class Create_hour(forms.ModelForm):
	hour_chance = forms.TimeField(label="Hora de chance", widget=forms.TextInput(attrs={'placeholder': 'formato: 02:03:AM o PM'}))
	hour_lesson = forms.TimeField(label="Hora de la clase", widget=forms.TextInput(attrs={'placeholder': 'formato: 02:03:AM o PM'}))
	hour_end = forms.TimeField(label="Hora de finalización de la clase", widget=forms.TextInput(attrs={'placeholder': 'formato: 02:03:AM o PM'}))
	primary_key_exercise = forms.IntegerField(widget=forms.HiddenInput())

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