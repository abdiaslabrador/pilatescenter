from django.urls import path

from . import views
app_name='devolution'

urlpatterns = [
	path('', views.DevolutionDecideView.as_view(), name='decide_devolution'),

	path('users_notreturned/', views.DevolutionNotReturnedUsersView.as_view(), name='users_notreturned_devolution'),
	path('notreturned_list/<int:id_user>/', views.NotReturnedListView.as_view(), name='notreturned_list_devolution'),
	path('see_notreturned/<int:id_devolution>/', views.DevolutionSeeView.as_view(template_name= 'devolution/devolution_notreturned.html'), name='devolution_see_notreturned'),

	path('users_returned/', views.DevolutionReturnedUsersView.as_view(), name='users_returned_devolution'),	
	path('returned_list/<int:id_user>/', views.ReturnedListView.as_view(), name='returned_list_devolution'),
	path('see_returned/<int:id_devolution>/', views.DevolutionSeeView.as_view(template_name= 'devolution/devolution_returned.html'), name='devolution_see_returned'),

	path('delete/<int:id_devolution>/', views.DevolutionDeleteView.as_view(), name='delete_devolution'),
	path('update_devolution/<int:id_lesson>/', views.UpdateDevolutionView.as_view(), name='update_devolution'),
	path('add_to_devolution/<int:id_lesson>/<int:id_user>/', views.AddToDevolutionView.as_view(), name='add_to_devolution'),
	path('takeout_to_devolution/<int:id_lesson>/<int:id_user>/', views.TakeOutToDevolutionView.as_view(), name='takeout_to_devolution'),
	path('takeout_users_in_class/<int:id_lesson>/<int:id_user>/', views.TakeOutToUsersLessonView.as_view(), name='takeout_users_in_class')
]	