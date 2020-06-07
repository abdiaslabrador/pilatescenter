from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField, UserChangeForm, UserCreationForm
from .models import CustomUser

class BaseUserAdmin(UserAdmin):

	form = UserChangeForm
	add_form = UserCreationForm

	model = CustomUser

	list_display = ('username',  'is_active', 'is_staff','is_superuser')
	list_filter = ('username', 'is_staff', 'is_active', 'is_staff')

	fieldsets = (
	('Username y contraseña (estas usando un username como identificador de usuario)', {'fields': ('username', 'password')}),
	('Información Personal ', {'fields': ('first_name', 'last_name','email','phone_number')}),
	('Permisos', {'fields': ('is_staff', 'is_active', 'is_superuser')}),
	)

	add_fieldsets = (
	(None, {
	'classes': ('wide',),
	'fields': ( 'username','first_name',  'last_name','email','phone_number',  'password1', 'password2',

				'is_staff','is_superuser')}
	),
	)

	search_fields = ('username',)
	ordering = ('username',)
	filter_horizontal = ()


admin.site.register(CustomUser, BaseUserAdmin)
