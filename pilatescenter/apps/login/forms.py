from django import forms
from apps.create_user.models import CustomUser

#esto es para el formulario del login-----------------
class LoginForm(forms.Form):

	username = forms.CharField(label='username', max_length=64)
	password = forms.CharField(label='Password', widget=forms.PasswordInput)


	def clean(self):
		#Check that the username and password will be correct
		cleaned_data=super().clean()

		username = cleaned_data.get("username")
		password = cleaned_data.get("password")

		if username is None:
			raise forms.ValidationError("Escriba un username")
		username = username.lower()

		try:
			user=CustomUser.objects.get(username=username)
		except CustomUser.DoesNotExist:
			raise forms.ValidationError("El username no existe.")
		
		if user.check_password(password) is not True:
			raise forms.ValidationError("Contraseña inválida.")

		cleaned_data['username'] = username
		return cleaned_data
