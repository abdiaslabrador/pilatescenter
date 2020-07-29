from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from apps.create_user.models import CustomUser

# I used this form to update the user
class UserUpdateForm(forms.ModelForm):

	class Meta:
		model = CustomUser
		fields = (
					"first_name",
					"last_name",
					"ci",
					"phone_number",
					"email",
				  )

# I used this form to change the password
class ChangePasswordForm(forms.ModelForm):
	password = forms.CharField(label='Password', widget=forms.PasswordInput)
	password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

	class Meta:
		model = CustomUser
		fields = (
					"password",
				  )

	def clean_password2(self):
		# Check that the two password entries match
		password = self.cleaned_data.get("password")
		password2 = self.cleaned_data.get("password2")
		if password and password2 and password != password2:
			raise forms.ValidationError("Contraseñas no coinciden")
		return password2