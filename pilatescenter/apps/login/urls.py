from django.urls import path

from . import views
app_name='admin_login'

urlpatterns = [
    path('login_admin', views.AdminLoginView.as_view(), name='login_admin'),
    path('logout_admin/', views.AdminLogoutView.as_view(), name='logout_admin')
]
