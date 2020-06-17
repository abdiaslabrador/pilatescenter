from django import forms
from .models import Exercise_det


class ConfirationUserPlanForm(forms.ModelForm):
    class Meta:
		model = Exercise_det
		fields = (
					"total_days",
					"oportunities",
					"enable_lessons",
					"scheduled_lessons",
					"saw_lessons",
                    "bag",
				  )
