from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from .models import CustomUser

# I used this form to create a user
class UserCreationForm(forms.ModelForm):

	password = forms.CharField(label='Password', widget=forms.PasswordInput)
	password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

	class Meta:
		model = CustomUser
		fields = (
					"username",
					"first_name",
					"last_name",
					"ci",
					"phone_number",
				  )

	def clean_username(self):
		username = self.cleaned_data.get("username")
		if username is None:
			raise forms.ValidationError("Escriba un nombre de usuario")

		username = username.lower()
		try:
			user=CustomUser.objects.get(username__iexact=username)
		except CustomUser.DoesNotExist:
			return username

		raise forms.ValidationError("El username ya existe")


	def clean_password2(self):
		# Check that the two password entries match
		password = self.cleaned_data.get("password")
		password2 = self.cleaned_data.get("password2")
		if password and password2 and password != password2:
			raise forms.ValidationError("Contraseñas no coinciden")
		return password2


	def save(self, commit=True):
	# Save the provided password in hashed format
		user = super().save(commit=False)
		user.set_password(self.cleaned_data["password"])
		if commit:
			user.save()
		return user

# I used this form to update the user
class UserUpdateForm(forms.ModelForm):
	#This variable is used to get the user to later check his information
	primarykey = forms.IntegerField(widget=forms.HiddenInput())
	class Meta:
		model = CustomUser
		fields = (
					"username",
					"first_name",
					"last_name",
					"ci",
					"phone_number",
				  )
	#this validation check if exist another user with the username wheter in lower case
	#or in upper case
	def clean(self):
		#here we have the username and the id
		clean = super().clean()
		username 	= self.cleaned_data.get("username")
		primarykey 	= self.cleaned_data.get("primarykey")

		if username is None:
			raise forms.ValidationError("Escriba un nombre de usuario")

		username = username.lower()

		#this part compare if the username written is the same that was already
		user = CustomUser.objects.get(pk=primarykey)
		if username == user.username.lower():
			self.cleaned_data['username']=username
			return clean

		#if it wasn't i compare the username with other usernames
		users = CustomUser.objects.exclude(pk=primarykey)

		for user in users:
			if username == user.username.lower():
				raise forms.ValidationError("Ya este username lo posee otro usuario")

		self.cleaned_data['username']=username
		return clean

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

class SearchClasses(forms.Form):
	since = forms.DateField(required=True)
	until = forms.DateField(required=True)