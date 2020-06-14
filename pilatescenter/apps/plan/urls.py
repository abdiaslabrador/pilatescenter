from django.urls import path

from . import views
app_name='Plan'

urlpatterns = [
	path('', views.ListPlanView.as_view(), name='list_plan'),
    path('create_plan/', views.CreatePlanView.as_view(), name='create_plan_form'),
    path('update_plan/<int:pk>/', views.UpdatePlanView.as_view(), name='update_plan_form'),
    path('delete_plan/<int:pk>/', views.DeletePlanView.as_view(), name='delete_plan'),
    path('see_plan/<int:pk>/', views.See.as_view(), name='see_plan'),
]