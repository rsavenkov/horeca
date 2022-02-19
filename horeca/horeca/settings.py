import os
import logging

from pathlib import Path


logging.basicConfig(
    format='%(asctime)s - %(message)s',
    level=logging.DEBUG,
)

BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ['HORECA_SECRET_KEY']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = eval(os.environ['HORECA_DEBUG'])

ALLOWED_HOSTS = os.environ['HORECA_ALLOWED_HOSTS']
CORS_ORIGIN_ALLOW_ALL = True


THIRD_PARTY_PACKAGES = [
    'rest_framework',
    'rest_framework.authtoken',
    'django_rest_passwordreset',
    'corsheaders',
    'django_filters',
    'multiselectfield',
]

PROJECT_APPS = [
    'users',
    'candidate_tests',
]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    *THIRD_PARTY_PACKAGES,
    *PROJECT_APPS,
]

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'users.authentication.ExpiringTokenAuthentication',
    ],
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend'
    ],
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'corsheaders.middleware.CorsMiddleware',
]

ROOT_URLCONF = 'horeca.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'horeca.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ['HORECA_DB_NAME'],
        'USER': os.environ['HORECA_DB_USER'],
        'PASSWORD': os.environ['HORECA_DB_PASSWORD'],
        'HOST': os.environ['HORECA_DB_HOST'],
        'PORT': os.environ['HORECA_DB_PORT'],
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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

AUTH_USER_MODEL = 'users.User'
EMAIL_HOST = os.environ['HORECA_EMAIL_HOST']
EMAIL_HOST_USER = os.environ['HORECA_EMAIL_HOST_USER']
EMAIL_HOST_PASSWORD = os.environ['HORECA_EMAIL_HOST_PASSWORD']
EMAIL_PORT = int(os.environ['HORECA_EMAIL_PORT'])
EMAIL_USE_TLS = eval(os.environ['HORECA_EMAIL_USE_TLS'])

DEFAULT_FROM_EMAIL = 'КорпУнивер «Мой бизнес» <' + os.environ['HORECA_EMAIL_HOST_USER'] + '>'

# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

STATIC_URL = os.environ['HORECA_STATIC_URL']
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# TODO: AHC-268 перенести все на s3
MEDIA_URL = '/api/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Время жизни токена
TOKEN_EXPIRED_AFTER_HOURS = 8
