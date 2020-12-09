"""
Django settings for pilatescenter project.

Generated by 'django-admin startproject' using Django 3.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE_DIR = os.path.join(BASE_DIR, "templates")

#nuestro modelo de usuario personalizado
AUTH_USER_MODEL = 'create_user.CustomUser'

 #aqí colocamos todas las rutas donde queremos que django busque todos archivos
STATICFILES_DIRS = [
                        os.path.join(BASE_DIR, "static"),
                    ]




# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'e%nk7eywmb1t6_35dp(4dd51^gw-l-shbopdsq&f-h%ykuk0vc'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'apps.login',
    'apps.create_user',
    'apps.plan',
    'apps.devolution',
    'apps.exercise',
    'apps.exercise_det',
    'apps.lesson_det',
    'apps.system',
    'apps.user_site.user_login',
    'apps.user_site.user_home',
    'apps.user_site.user_lesson_list',
    'apps.user_site.user_profile',

]
# 'apps.history_det',

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10
}


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'pilatescenter.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATE_DIR],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'pilatescenter.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'pilatescenter',
        'USER': 'postgres',
        'PASSWORD': '****',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'es-ve'

TIME_ZONE =     'America/Caracas' #'UTC'

USE_I18N = True

USE_L10N = False

USE_TZ = True

TIME_INPUT_FORMATS= ['%I:%M:%p']

#email
EMAIL_HOST= 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS= True
EMAIL_HOST_USER= 'projects.testing.email@gmail.com'
EMAIL_HOST_PASSWORD= 'Dani1993?3'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

#/static/ es el directorio de principal para archivos css y javascript, que trabaja con
#STATICFILES_DIRS para pasarle los archivos a static_root
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'trans_static_al_servidor')

# CELERY STUFF
BROKER_URL = 'redis://localhost:6379'
CELERY_RESULT_BACKEND = 'redis://localhost:6379'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = TIME_ZONE