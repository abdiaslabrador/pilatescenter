from django.urls import path

from . import views
app_name='user_home'

urlpatterns = [
    path('', views.user_home.as_view(), name='user_home')
]
