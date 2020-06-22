from django.urls import path

from . import views
app_name='lesson'

urlpatterns = [
	path('list_hour/<int:pk>/', views.ListHourView.as_view(), name='list_hour'),
	path('create_hour/<int:pk>/', views.CreateHourView.as_view(), name='create_hour'),
	path('update_hour/<int:pk>/', views.UpdateHourView.as_view(), name='update_hour'),
	path('delete_hour/<int:pk>/', views.DeleteHourView.as_view(), name='delete_hour')
]
	