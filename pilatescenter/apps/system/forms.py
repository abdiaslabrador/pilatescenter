from django import forms
from .models import SystemPilates, Contact
from django.core.exceptions import ValidationError

class SystemPilatesForm(forms.ModelForm):
	delta_day = forms.IntegerField(label='Dias que podrá ver el usuario a escoger', required=True, min_value=0, max_value=31)
	cant_max = forms.IntegerField(label='Cantidad máxima por clase', required=True, min_value=0, max_value=10)
	
	class Meta:
		model= SystemPilates
		fields= (
					"delta_day",
					"cant_max",
					"reglas",

				)
	def __init__(self, *args, **kwargs):
	    super().__init__(*args, **kwargs)
	    self.fields['reglas'].widget.attrs.update({'label':'Reglas','rows': '20', 'cols':"120"})

class SystemContactForm(forms.ModelForm):
	class Meta:
		model= Contact
		fields= (
					"email",
					"phone_number",
					"direction",
					

				)
	def __init__(self, *args, **kwargs):
	    super().__init__(*args, **kwargs)
	    self.fields['direction'].widget.attrs.update({'rows': '10', 'cols':"60"})