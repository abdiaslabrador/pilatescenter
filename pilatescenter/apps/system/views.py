#generals for tests
from django.http import HttpResponse

#spedific for this view
from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
#models
from .models import SystemPilates, Contact
from .forms import SystemPilatesForm, SystemContactForm

# Create your views here.
class SystemConfigurationView(View):
	template_name= 'systempilates/systempilates.html'

	def post(self, request, *args, **kwargs):
		
		#validacion de que sea un superusuario
		if not request.user.is_superuser:
			return redirect('login:login')

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
		
		#validacion de que sea un superusuario
		if not request.user.is_superuser:
			return redirect('login:login')

		system = SystemPilates.objects.order_by('id').first()
		if system == None:
			system = SystemPilates.objects.create()

		form = SystemPilatesForm(instance = system)

		context = {
					'form':form
				}
		return render(request, self.template_name, context)


# Create your views here.s
class SystemContactView(View):
	template_name= 'systempilates/contact.html'

	def post(self, request, *args, **kwargs):

		#validacion de que sea un superusuario
		if not request.user.is_superuser:
			return redirect('login:login')

		contact = Contact.objects.order_by('id').first()
		if contact == None:
			contact = Contact.objects.create()

		form = SystemContactForm(request.POST, instance=contact)

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
		
		#validacion de que sea un superusuario
		if not request.user.is_superuser:
			return redirect('login:login')

		contact = Contact.objects.order_by('id').first()
		if contact == None:
			contact = Contact.objects.create()

		form = SystemContactForm(instance = contact)

		context = {
					'form':form
				}
		return render(request, self.template_name, context)