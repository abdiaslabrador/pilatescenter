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
    path('exercise_configuration/<int:pk>/', views.ExerciseConfigurationView.as_view(), name='exercise_configuration'),
    path('listado/', views.listado, name="list_user_json"),
    path('UserAPI/', views.UserAPI.as_view(), name="list_user_api")

]
