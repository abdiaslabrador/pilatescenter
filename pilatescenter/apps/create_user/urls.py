from django.urls import path


from . import views

app_name="content_user"
urlpatterns = [
    path('', views.ListUserView.as_view(), name="list_user"),
    path('create_user/', views.create_user, name="create_user_form"),
    path('modific_user/<int:pk>/', views.modific_user, name="modific_user_form"),
    path('delete_user/<int:pk>/', views.DeleteUserView.as_view(), name='delete_user'),
    path('change_password_user/<int:pk>/', views.change_password_user, name="change_password_form"),
    path('list_locked_user/', views.ListLockedUserView.as_view(), name="list_locked_user"),
    path('lock_user/<int:pk>/', views.LockUserView.as_view(), name="lock_user"),
    path('unlock_user/<int:pk>/', views.UnlockUserView.as_view(), name="unlock_user"),
    path('user_configuration_class/<int:pk>/', views.UserConfigurationClassView.as_view(), name='user_configuration_class'),
    path('saw_lesson/<int:id_lesson>/<int:id_exercise_det>/', views.UserConfigurationSawLessonView.as_view(), name='saw_lesson'),
    path('delete_lesson/<int:id_lesson>/<int:id_exercise_det>/', views.DeleteLessonView.as_view(), name='delete_lesson'),
    path('user_configuration_plan/<int:pk>/', views.UserConfigurationPlanView.as_view(), name='user_configuration_plan'),
    path('user_configuration_change_plan/change_plan/<int:pk>/', views.UserConfigurationChangePlanView.as_view(), name='user_configuration_change_plan'),
    path('user_configuration_history/<int:pk>/', views.UserConfigurationHistoryView.as_view(), name='user_configuration_history'),
    path('user_configuration_reset/<int:pk>/', views.UserConfigurationResetView.as_view(), name='user_configuration_reset'),
    path('reset/<int:pk>/', views.ResetUsersView.as_view(), name='reset_users'),
    path('listado/', views.listado, name="list_user_json"),
    path('UserAPI/', views.UserAPI.as_view(), name="list_user_api")

]
