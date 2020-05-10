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
				"id_exercise_fk",
				)

	def clean(self):
		cleaned_data = super(CreatePlanForm, self).clean()

		name = cleaned_data.get('name')
		id_exercise_fk = cleaned_data.get('id_exercise_fk')
		
		if name is None:
			raise forms.ValidationError("Escriba un nombre para el plan")

		try:
			r=Plan.objects.get(name__icontains=name, id_exercise_fk=id_exercise_fk)
		except Plan.DoesNotExist:
			name=name.upper()
			cleaned_data['name']=name
			return cleaned_data
	
		if r:			
			raise forms.ValidationError("El nombre del plan que desea registrar ya existe con este ejercicio")



class UpdatePlanForm(forms.ModelForm):
	primarykey 		= forms.IntegerField(widget=forms.HiddenInput())
	id_exercise_fk	= forms.ModelChoiceField(queryset=Exercise.objects.all(), widget=forms.HiddenInput())
	class Meta:
		model= Plan
		fields= (
				"name",
				"total_days",
				"oportunities",
				"id_exercise_fk",
				)

	def clean(self):
		clean = super(UpdatePlanForm, self).clean()

		name  = self.cleaned_data.get('name')
		exercise_obj = self.cleaned_data.get('id_exercise_fk')
		primarykey 	 = self.cleaned_data.get("primarykey")

		if name is None:
			raise forms.ValidationError("Escriba un nombre para el plan")
		
		name = name.lower()

		plan = Plan.objects.get(pk=primarykey)
		if name.lower() == plan.name.lower():
			self.cleaned_data['name']=name.upper()
			return clean

		plans = Plan.objects.filter(id_exercise_fk=exercise_obj.pk).exclude(id=primarykey)
		
		for plan in plans:
			if name == plan.name.lower():
				raise forms.ValidationError("Ya este plan existe este tipo de ejercicio")

		self.cleaned_data['name']=name.upper()
		return clean		