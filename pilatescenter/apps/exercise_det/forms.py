from django import forms
from .models import Exercise_det



class ConfigurationUserExerciseForm(forms.ModelForm):
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

class ConfigurationUserChangePlanForm(forms.ModelForm):
    class Meta:
        model = Exercise_det
        fields = (
        			"id_plan_fk",
        		  )


class ConfigurationUserResetForm(forms.ModelForm):
    class Meta:
        model = Exercise_det
        fields = (
        			"reset",
        		  )
