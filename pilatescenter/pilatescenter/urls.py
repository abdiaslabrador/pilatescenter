"""pilatescenter URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path
from django.contrib import admin
from apps.login.views import LoginView, LogoutView
from rest_framework.authtoken import views
from django.contrib.auth.views import ( 
                                        PasswordResetView, PasswordResetDoneView, 
                                        PasswordResetConfirmView, PasswordResetCompleteView
                                      )

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', include('apps.login.urls')),
    path('plan/', include('apps.plan.urls')),
    path('exercise/', include('apps.exercise.urls')),
    path('users/', include('apps.create_user.urls')),
    path('lesson/', include('apps.lesson_det.urls')),
    path('history/', include('apps.history_det.urls')),
    path('devolution/', include('apps.devolution.urls')),
    path('systempilates/', include('apps.system.urls')),


    path('user_site/home/', include('apps.user_site.user_home.urls')),
    path('user_site/lessons/', include('apps.user_site.user_lesson_list.urls')),
    path('user_site/profile/', include('apps.user_site.user_profile.urls')),

    path('password_reset/', PasswordResetView.as_view(template_name='password_reset/password_reset_form.html', email_template_name='password_reset/password_reset_email.html'), name= 'password_reset'),
    path('password_reset/done/', PasswordResetDoneView.as_view(template_name='password_reset/password_reset_done.html'), name= 'password_reset_done'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name='password_reset/password_reset_confirm.html'), name= 'password_reset_confirm'),
    path('reset/done/', PasswordResetCompleteView.as_view(template_name='password_reset/password_reset_complete.html'), name= 'password_reset_complete'),
    
    path('api-token-auth/', views.obtain_auth_token)
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

    # path('user_site/', include('apps.history_det.urls')),
    