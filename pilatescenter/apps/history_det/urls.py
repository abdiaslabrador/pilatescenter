from django.urls import path

from . import views
app_name='history'

urlpatterns = [
	path('list_lesson_exercise_history/', views.ListLessonExerciseHistoryView.as_view(), name='list_lesson_exercise_history'),	
	path('list_history/<int:pk>/', views.ListHistoryView.as_view(), name='list_history'),
	path('see_history/<int:pk>/', views.SeeHistoryView.as_view(), name='see_history'),
	path('delete_history/<int:id_history>/', views.DeleteHistoryView.as_view(), name='delete_history'),
]	
