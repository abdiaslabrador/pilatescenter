from django.urls import path

from . import views
app_name='history'

urlpatterns = [
	path('list_lesson_exercise_history/', views.ListLessonExerciseHistoryView.as_view(), name='list_lesson_exercise_history'),	
	path('list_history/<int:id_exercise>/', views.ListHistoryView.as_view(), name='list_history'),
	path('general_see_history/<int:id_history>/<int:id_exercise>/', views.GeneralSeeHistoryView.as_view(), name='general_see_history'),
	path('general_delete_history/<int:id_history>/<int:id_exercise>/', views.GeneralDeleteHistoryView.as_view(), name='general_delete_history'),
	path('see_history/<int:id_history>/<int:id_exercise_det>', views.UserConfigurationSeeHistoryView.as_view(), name='see_history'),
	path('delete_history/<int:id_history>/<int:id_exercise_det>', views.UserConfigurationDeleteHistoryView.as_view(), name='delete_history'),
]	
