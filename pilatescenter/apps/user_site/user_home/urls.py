from django.urls import path

from . import views
app_name='user_home'

urlpatterns = [
    path('', views.UserHomeView.as_view(), name='user_home'),
    path('contact/', views.UserContactView.as_view(), name='contact'),
    path('rules/', views.UserRulesView.as_view(), name='rules')
]
