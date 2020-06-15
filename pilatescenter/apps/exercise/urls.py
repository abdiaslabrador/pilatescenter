from django.urls import path

from . import views
app_name='exercise'

urlpatterns = [
	path('', views.ListExerciseView.as_view(), name='list_exercise'),
	path('create_exercise/', views.CreateExerciseView.as_view(), name='create_exercise_form'),
	path('update_exercise/<int:pk>/', views.UpdateExerciseView.as_view(), name='update_exercise_form'),
	path('delete_exercise/<int:pk>/', views.DeleteExerciseView.as_view(), name='delete_exercise'),
	path('see_exercise/<int:pk>/', views.See.as_view(), name='see_exercise'),
]
