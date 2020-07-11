from django import forms



class SearchClasses(forms.Form):
	since = forms.DateField(required=True)
	until = forms.DateField(required=True)