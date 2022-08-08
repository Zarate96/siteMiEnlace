import os
from decouple import config
from miEnlace.settings.base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['mienlacemexico.com']


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

SITE_URL = 'https://mienlacemexico.com'
PROTOCOL_HTTP = 'https'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db.sqlite3',
    }
}

