from django import forms
from .models import Exercise_det
from apps.lesson_det.models import Lesson_det


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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['scheduled_lessons'].widget.attrs.update({'readonly': 'readonly',  'min':0, 'max':28})
        self.fields['enable_lessons'].widget.attrs.update({'readonly': 'readonly',  'min':0, 'max':28})
        self.fields['saw_lessons'].widget.attrs.update({'readonly': 'readonly',  'min':0, 'max':28})
        self.fields['bag'].widget.attrs.update({'readonly': 'readonly',  'min':0, 'max':28})

    def clean(self):
        clean = super().clean()
        total_days    = self.cleaned_data.get("total_days")
        scheduled_lessons = self.cleaned_data.get("scheduled_lessons")
        saw_lessons    = self.cleaned_data.get("saw_lessons")

    

        if total_days < (scheduled_lessons + saw_lessons):
            
            raise forms.ValidationError("La cantidad de días disponibles no puede ser menor que la suma de días programados, vistos y en bolsa")

        return clean

class ConfigurationUserChangePlanForm(forms.ModelForm):
    

    class Meta:
        model = Exercise_det
        fields = (
                    "id_plan_fk",
                    "id_exercise_fk",
                    "id_user_fk",
        		  )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['id_user_fk'].widget.attrs.update({'hidden': 'True'})
        self.fields['id_exercise_fk'].widget.attrs.update({'hidden': 'True'})

    def clean(self):
        clean = super().clean()
        id_user_fk    = self.cleaned_data.get("id_user_fk")
        id_exercise_fk = self.cleaned_data.get("id_exercise_fk")

        cant_lesson_scheduled = Lesson_det.objects.filter(id_exercise_fk= id_exercise_fk.id, id_user_fk= id_user_fk.id, saw= False).count()

        if cant_lesson_scheduled > 0:
            #el error de abajo no sale porque tube que marañar con un mensaje de aviso de boostrap
            raise forms.ValidationError("El usuario tiene almenos 1 clase programada, y no se puede reiniciar con clases programadas. ESTE ERROR NO SALE, LEE EL COMENTARIO")

        return clean





class ConfigurationUserResetForm(forms.ModelForm):
    class Meta:
        model = Exercise_det
        fields = (
        			"reset",
                    "id_exercise_fk",
                    "id_user_fk",
        		  )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['id_user_fk'].widget.attrs.update({'hidden': 'True'})
        self.fields['id_exercise_fk'].widget.attrs.update({'hidden': 'True'})

    def clean(self):
        clean = super().clean()
        reset = self.cleaned_data.get("reset")
        id_user_fk    = self.cleaned_data.get("id_user_fk")
        id_exercise_fk = self.cleaned_data.get("id_exercise_fk")

        cant_lesson_scheduled = Lesson_det.objects.filter(id_exercise_fk= id_exercise_fk.id, id_user_fk= id_user_fk.id, saw= False).count()
        if reset == False:
            if cant_lesson_scheduled > 0:
                #el error de abajo no sale porque tube que marañar con un mensaje de aviso de boostrap
                raise forms.ValidationError("El usuario tiene almenos 1 clase programada. Para habilitar la opción 'No reiniciar' el usuario no puede tener clases programadas.")

        return clean