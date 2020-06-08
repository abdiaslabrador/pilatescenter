from django.urls import path


from . import views

app_name="content_user"
# path('', views.ListUserView.as_view(), name="list_user")
urlpatterns = [

    path('create_user/', views.create_user, name="create_user_form"),
    path('modific_user/<int:pk>/', views.modific_user, name="modific_user_form"),
    path('change_password_user/<int:pk>/', views.change_password_user, name="change_password_form"),
    path('listado/', views.listado, name="list_user_json"),
    path('UserAPI/', views.UserAPI.as_view(), name="list_user_api")

]
