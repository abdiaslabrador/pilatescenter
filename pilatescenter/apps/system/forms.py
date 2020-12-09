from django import forms
from .models import SystemPilates
from django.core.exceptions import ValidationError

class SystemPilatesForm(forms.ModelForm):
	delta_day = forms.IntegerField(label='Dias que podrá ver el usuario a escoger', required=True, min_value=0, max_value=31)
	cant_max = forms.IntegerField(label='Cantidad máxima por clase', required=True, min_value=0, max_value=10)

	class Meta:
		model= SystemPilates
		fields= (
					"delta_day",
					"cant_max",
				)