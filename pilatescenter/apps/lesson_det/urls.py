from django.urls import path

from . import views
app_name='lesson'

urlpatterns = [
	path('create_lesson/', views.CreateLessonView.as_view(), name='create_lesson_form'),
	path('busqueda/<int:pk>/<int:year>/<int:month>/<int:day>/', views.CreateLessonSearchView.as_view(), name='create_lesson_form_search'),
	path('list_lesson_exercise_action/', views.ListLessonExerciseActionView.as_view(), name='list_lesson_exercise_action'),
	path('list_lesson/<int:pk>/', views.ListLessonView.as_view(), name='list_lesson'),
	path('update_lesson/<int:pk>/', views.UpdateLessonView.as_view(), name='update_lesson'),
	path('add_to_lesson/<int:id_lesson>/<int:id_user>/', views.AddToLessonView.as_view(), name='add_to_lesson'),
	path('takeout_to_lesson/<int:id_lesson>/<int:id_user>/', views.TakeOutToLessonView.as_view(), name='takeout_to_lesson'),
	path('sawlesson/<int:id_lesson>/', views.SawLessonView.as_view(), name='sawlesson'),
	path('delete_lesson/<int:id_lesson>/', views.DeleteLessonView.as_view(), name='delete_lesson')
	
]	