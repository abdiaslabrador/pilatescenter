from django import forms
from apps.exercise.models import Day


#------------------------------------------------------------------------------------------
#lesson
#------------------------------------------------------------------------------------------
class SearchLessonForm(forms.Form):
	day =forms.ModelChoiceField(
									label = "Selecccione día:",
									required=True,
									queryset=Day.objects.all().order_by("name")
								)
	