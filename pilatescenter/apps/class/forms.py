from django import forms
from .models import class

class CreateClassForm(forms.ModelForm):
	class Meta:
		model = Class
		
