from .base import *

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'this-is-a-test-key'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1', '[::1]']

CORS_ORIGIN_WHITELIST = ['http://localhost:8080']

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'test',
        'USER': 'graphery',
        'PASSWORD': 'graphery',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}

# Debug middleware
# _debug {
#     sql {
#       rawSql
#     }
#   }
GRAPHENE.get('MIDDLEWARE', []).append('graphene_django.debug.DjangoDebugMiddleware')
