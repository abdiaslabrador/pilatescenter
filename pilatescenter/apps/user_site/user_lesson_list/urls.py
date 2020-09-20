from django.urls import path
from . import views

app_name='user_lesson'

urlpatterns = [
    path('<int:id_exercise>/', views.UserLessonListView.as_view(), name='lesson_list'),
    path('resumen/<int:id_exercise_det>/', views.UserResumenView.as_view(), name='resumen'),
    path('inbag/<int:id_lesson>/<int:id_exercise_det>/', views.UserInBagView.as_view(), name='inbag'),#reserva de clases
    path('bag/<int:id_exercise_det>/', views.UserBagView.as_view(), name='bag'),#lista de las clases que se pueden escojer
    path('bag_day_selected/<int:id_lesson>/', views.UserBagDaySelectedView.as_view(), name='bag_day_selected'),
]
