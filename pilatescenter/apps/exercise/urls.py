from django.urls import path

from . import views
app_name='exercise'

urlpatterns = [
	path('', views.ListExerciseView.as_view(), name='list_exercise'),
	path('create_exercise/', views.CreateExerciseView.as_view(), name='create_exercise_form'),
	path('update_exercise/<int:pk>/', views.UpdateExerciseView.as_view(), name='update_exercise_form'),
	path('delete_exercise/<int:pk>/', views.DeleteExerciseView.as_view(), name='delete_exercise'),
	path('see_exercise/<int:pk>/', views.See.as_view(), name='see_exercise'),
	path('list_day/<int:pk>/', views.ListDayView.as_view(), name='list_day'),
	path('create_day/<int:pk>/', views.CreateDayView.as_view(), name='create_day'),
	path('delete_day/<int:pk>/<int:id_day>/', views.DeleteDayView.as_view(), name='delete_day'),
	path('list_hour/<int:pk>/<int:id_day>/', views.ListHourView.as_view(), name='list_hour'),
	path('create_hour/<int:pk>/<int:id_day>/', views.CreateHourView.as_view(), name='create_hour'),
	path('update_hour/<int:pk>/<int:id_day>/', views.UpdateHourView.as_view(), name='update_hour'),
	path('delete_hour/<int:pk>/<int:id_day>/', views.DeleteHourView.as_view(), name='delete_hour'),
	
]
