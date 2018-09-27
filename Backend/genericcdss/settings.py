"""
Django settings for genericcdss project.

Generated by 'django-admin startproject' using Django 1.11.10.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '5xl1*t=-qz1a)+*)#3zo$1+v_n)#dz8d72jco80w48dco3)gt)'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
    '*'
    #'.127.0.0.1',  # Allow domain and subdomains
    #'.127.0.0.1.',  # Also allow FQDN and subdomains,
    #'localhost'

]

CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True

ADMINS = (
    ('Joao Rafael Almeida', 'joao.rafael.almeida@ua.pt'),
)

SITE_NAME = "Generic CDSS"

ADMIN_CONSOLE_NAME = SITE_NAME + " Admin"
# Application definition

INSTALLED_APPS = [
    'jet.dashboard',
    'jet',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    #models
    'accounts',
    'history',
    'patients',
    'protocol',
    'protocol_element',
    'utils',

	'constance',
    'constance.backends.database',

    'django.contrib.sites',
    'django.contrib.flatpages',

    'rest_framework',
    'corsheaders',
    'django_filters'
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware'
    #'corsheaders.middleware.CorsMiddleware',
]

ROOT_URLCONF = 'genericcdss.urls'

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
        },
    },
]

WSGI_APPLICATION = 'genericcdss.wsgi.application'

REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10000,
    'DATE_FORMAT': "%d/%m/%Y",
}

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': os.environ.get('DOCKER_POSTGRES_DB', 'genericcdss'), # Or path to database file if using sqlite3.
        'USER': os.environ.get('DOCKER_POSTGRES_USER', 'genericcdss'), # Not used with sqlite3.
        'PASSWORD': os.environ.get('DOCKER_POSTGRES_PASS', '12345'), # Not used with sqlite3.
        'HOST': os.environ.get('DOCKER_POSTGRES_HOST', 'localhost'), # Set to empty string for localhost. Not used with sqlite3.
        'PORT': os.environ.get('DOCKER_POSTGRES_PORT', '5432'), # Set to empty string for default. Not used with sqlite3.
    },
}


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'WET'

USE_I18N = True

USE_L10N = True

#USE_TZ = True

SITE_ID = 1

SESSION_COOKIE_NAME = os.environ.get('SESSION_COOKIE_NAME', 'genericcdss')


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'

#Authentication backends
AUTHENTICATION_BACKENDS = (
        'django.contrib.auth.backends.ModelBackend',
    )

GLOBALS = {
    'SITE_NAME': SITE_NAME,
    'COPYRIGHT': "Bioinformatics.UA, UA",
    'FOOTER_EXTRA': """<a href='http://www.ua.pt/'>
                    <img style='margin-left:20px' src='https://emif-catalogue.eu/taska/static/images/logo-ua2.png'>
                    </a>""",
    'APP_SYMBOL':"""
                    <img style='margin-left:20px' src='static/NOTFOUND'>
                 """,
    'LANGUAGE':"pt - to do"
}

CONSTANCE_BACKEND = 'constance.backends.database.DatabaseBackend'

CONSTANCE_CONFIG = {
    'copyright': (GLOBALS['COPYRIGHT'], 'Text to show as copyright'),
    'copyrightsplash': ('<a target="_blank" href="http://bioinformatics.ua.pt/">Bioinformatics, UA.</a>', 'Text to show as copyright on splash screen'),
    'footer_extra': (GLOBALS['FOOTER_EXTRA'], 'Extra HTML to be shown besides the footer'),
    'app_symbol': (GLOBALS['APP_SYMBOL'], 'Image used to represent the system (Logo)'),
    'site_name': (GLOBALS['SITE_NAME'], 'Website title'),
    'language':(GLOBALS['LANGUAGE'], 'The languge used in the GUI')
}

CONSTANCE_CONFIG_FIELDSETS = {
    'General Options': ('site_name', 'footer_extra', 'app_symbol', 'copyrightsplash', 'copyright','language'),
}

JET_DEFAULT_THEME = 'light-blue'
