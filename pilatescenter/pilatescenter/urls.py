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

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view()),
    path('plan/', include('apps.plan.urls')),
    path('exercise/', include('apps.exercise.urls')),
    path('users/', include('apps.create_user.urls')),
    path('lesson/', include('apps.lesson_det.urls')),
    path('history/', include('apps.history_det.urls')),
    path('api-token-auth/', views.obtain_auth_token)
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
