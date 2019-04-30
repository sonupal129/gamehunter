"""
Django settings for gamehunter project.

Generated by 'django-admin startproject' using Django 2.0.1.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '@aju5^l81trvsenrh%3lw^c$6i1_vnb^zqxpd&2$j#$!03s_ao'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1']

# Application definition

INSTALLED_APPS = [
    'shop.apps.ShopConfig',
    'carts.apps.CartsConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.sitemaps',
    'django.contrib.redirects',
    # other apps
    'treebeard',
    'adminsortable',
    'ckeditor',
    'post_office',
    'django_slack',
    'background_task',
    'sorl.thumbnail',
    # 'compressor',

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.redirects.middleware.RedirectFallbackMiddleware',
    # Other Middle ware classed
    'htmlmin.middleware.HtmlMinifyMiddleware',
    'htmlmin.middleware.MarkRequestMiddleware',


]

ROOT_URLCONF = 'gamehunter.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            # 'loaders': [
            #     'django.template.loaders.app_directories.Loader',
            # ],
        },
    },
]

WSGI_APPLICATION = 'gamehunter.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'hunterdatabase',
        'USER': 'postgres',
        'PASSWORD': '123456',
        'HOST': 'localhost'
    }
}

# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Calcutta'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

# Ck-Editor Config Settings

CKEDITOR_CONFIGS = {
    'default': {
    'toolbar': 'Custom',
        'toolbar_Custom': [
            ['Bold', 'Italic', 'Underline'],
            ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', '-', 'JustifyLeft', 'JustifyCenter',
             'JustifyRight', 'JustifyBlock'],
            ['Link', 'Unlink'],
            ['RemoveFormat', 'Source'],
            ['Image', 'HorizontalRule', 'Smiley', 'SpecialChar', 'Iframe', 'Iframe dialog'],
            ['Styles', 'Format', 'Font', 'FontSize'],
        ]
    }
}

CKEDITOR_UPLOAD_PATH = "uploads/"

# User Authentications
LOGIN_URL = "shop:login"
LOGIN_REDIRECT_URL = 'shop:homepage'
LOGOUT_REDIRECT_URL = 'shop:homepage'

# Email Backend - Current Provider Amazon SES
POST_OFFICE = {
    'BACKENDS': {
        'default': 'smtp.EmailBackend',
        'django_ses': 'django_ses.SESBackend',
    },
    'BATCH_SIZE': 100,
    'DEFAULT_PRIORITY': 'now',
}

AWS_ACCESS_KEY_ID = 'AKIAIXJMBDAJVH6XYS6A'
AWS_SECRET_ACCESS_KEY = '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'
# AWS_SES_REGION_NAME = 'us-east-1'
# AWS_SES_REGION_ENDPOINT = 'email-smtp.us-east-1.amazonaws.com'

# Slack API Token & Information for Notification
SLACK_TOKEN = 'xoxb-402668290307-541515247091-5kxEPnxOQ0dQSLy334WoENDE'

# Instamojo Payment Gateway Link Url
INSTAMOJO_API_KEY = "test_830b282750b49d50fb88d7e72c9"
INSTAMOJO_AUTH_TOKEN = "test_f544367f6405aa31283a4605731"
BASE_PAYMENT_URL = "https://test.instamojo.com/api/1.1/payment-requests/"
PAYEMENT_REDIRECT_URL = "http://127.0.0.1:8000/cart/payment/successful"

# Sitemaps Details
# if DEBUG:
SITE_ID = 2

# Django Caches
if not DEBUG:
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
            'LOCATION': 'd:/Game Hunter/testcache/',
            'TIMEOUT': 18000,
        }
    }

# django htmlmin
EXCLUDE_FROM_MINIFYING = ('url-optimize/sitemap.xml/', 'cki39vbl3/admin/')

# Django Logging for Refining SQL Queries
# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'handlers': {
#         'console': {
#             'class': 'logging.StreamHandler',
#         },
#     },
#     'loggers': {
#         'django.db.backends': {
#             'level': 'DEBUG',
#             'handlers': ['console'],
#         }
#     },
# }


try:
    from .local_settings import *
except ImportError:
    pass

