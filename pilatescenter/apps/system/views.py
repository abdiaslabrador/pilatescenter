#generals for tests
from django.http import HttpResponse

#spedific for this view
from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
#models
from .models import SystemPilates
from .forms import SystemPilatesForm

# Create your views here.
class SystemConfigurationView(View):
	template_name= 'systempilates/systempilates.html'

	def post(self, request, *args, **kwargs):
		
		system = SystemPilates.objects.order_by('id').first()
		if system == None:
			system = SystemPilates.objects.create()

		form = SystemPilatesForm(request.POST, instance=system)

		if form.is_valid():
			form.save()
			messages.success(request, 'Se han echo los cambios con éxito', extra_tags='alert-success')

			context = {
						'form':form
					}
					
			return render(request, self.template_name, context)
		else:

			context = {
						'form':form
					}
			return render(request, self.template_name, context)

	def get(self, request, *args, **kwargs):
		
		system = SystemPilates.objects.order_by('id').first()
		if system == None:
			system = SystemPilates.objects.create()

		form = SystemPilatesForm(instance = system)

		context = {
					'form':form
				}
		return render(request, self.template_name, context)