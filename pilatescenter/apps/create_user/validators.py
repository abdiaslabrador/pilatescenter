from django.core.exceptions import ValidationError


def name_space(value):
	username = value
	if username.count(" ") > 0:
		raise ValidationError("El username contiene espacios")

