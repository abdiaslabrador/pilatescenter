from django.urls import path

from . import views
app_name='user_login'

urlpatterns = [
    path('', views.UserLoginView.as_view(), name='user_login_form'),
    path('logout', views.UserLogoutView.as_view(), name='user_logout'),
]
'user_login:user_login_form'