from django.urls import path
from . import views

app_name='user_profile'

urlpatterns = [
    path('configuration/', views.UserConfigurationProfileView.as_view(), name='configuration_profile'),
    path('change_password_user/', views.UserChangePasswordView.as_view(), name="change_password_form"),
]
