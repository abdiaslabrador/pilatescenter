from django.urls import path
from . import views

app_name='systempilates'

urlpatterns = [
	path('system/', views.SystemConfigurationView.as_view(), name='main_system'),
]	