from django import forms
from .models import Plan
from apps.exercise.models import Exercise
from django.core.exceptions import ValidationError

class CreatePlanForm(forms.ModelForm):
	
	class Meta:
		model= Plan
		fields= (
					"name",
					"total_days",
					"oportunities",
					"description",
					"id_exercise_fk",

				)

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['id_exercise_fk'].widget.attrs.update({'hidden': 'True'})

		

	def clean(self):
		"""
			this function verify that the name written is unique in the database
		"""
		cleaned_data = super(CreatePlanForm, self).clean()
		
		name = cleaned_data.get('name')
		id_exercise_fk = cleaned_data.get('id_exercise_fk')

		#i assure that the name is not null
		if name is None:
			raise forms.ValidationError("Escriba un nombre para el plan")

		#after i got the name, i verify that the name not exist
		try:
			r=Plan.objects.get(name__iexact=name, id_exercise_fk=id_exercise_fk)
		except Plan.DoesNotExist:
			name=name.upper()
			cleaned_data['name']=name
			return cleaned_data

		#if exist, i rasise a error
		if r:			
			raise forms.ValidationError("El nombre del plan que desea registrar ya existe con este ejercicio")



class UpdatePlanForm(forms.ModelForm):
	primarykey 		= forms.IntegerField(widget=forms.HiddenInput())
	
	class Meta:
		model= Plan
		fields= (
					"name",
					"total_days",
					"oportunities",
					"description",
					"id_exercise_fk"
				)
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['id_exercise_fk'].widget.attrs.update({'hidden': 'True'})
		
	def clean(self):
		clean = super(UpdatePlanForm, self).clean()

		name  		 = self.cleaned_data.get('name') #name of the plan
		primarykey 	 = self.cleaned_data.get("primarykey") #pk of the plan
		exercise_obj = self.cleaned_data.get('id_exercise_fk') #types of the exercises
		

		if name is None:
			raise forms.ValidationError("Escriba un nombre para el plan")
		
		name = name.upper()

		"""i get the plan by the pk. Then i compare is the object is the same that i'm modifing,
		is so, i return the ocject.
		"""
		plan = Plan.objects.get(pk=primarykey)
		if name == plan.name.upper():
			self.cleaned_data['name']=name
			return clean

		"""if the object is not the same, i compare the object with other plan to comprabate if it doesn't exist.
		The query is: Give me all plan from a specific exercise but exclud me.
		"""
		plans = Plan.objects.filter(id_exercise_fk=exercise_obj.pk).exclude(id=primarykey)
		
		for plan in plans:
			if name == plan.name.upper():
				raise forms.ValidationError("Ya este plan existe este tipo de ejercicio")

		self.cleaned_data['name']=name.upper()
		return clean		