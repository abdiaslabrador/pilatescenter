from django.urls import path

from . import views
app_name='user_home'

urlpatterns = [
    path('', views.UserHomeView.as_view(), name='user_home')
]
