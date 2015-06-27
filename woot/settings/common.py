"""Common settings and globals."""

import site

from datetime import timedelta
from os.path import abspath, basename, dirname, join, normpath
from sys import path

from djcelery import setup_loader


########## PATH CONFIGURATION
# Absolute filesystem path to the Django project directory:
DJANGO_ROOT = dirname(dirname(abspath(__file__)))

# Absolute filesystem path to the top-level project folder:
SITE_ROOT = dirname(DJANGO_ROOT)

# Site name:
SITE_NAME = basename(DJANGO_ROOT)

# Add our project to our pythonpath, this way we don't need to type our project
# name in our dotted import paths:
path.append(DJANGO_ROOT)
########## END PATH CONFIGURATION


########## DEBUG CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = False

# See: https://docs.djangoproject.com/en/dev/ref/settings/#template-debug
TEMPLATE_DEBUG = DEBUG
########## END DEBUG CONFIGURATION


########## EMAIL CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
EMAIL_BACKEND = 'djrill.mail.backends.djrill.DjrillBackend'
########## END EMAIL CONFIGURATION


########## MANAGER CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#admins
ADMINS = (
    ('Siddardha Garimella', 'gsiddardha@makeystreet.com'),
    ('Alex J V', 'alex@makeystreet.com'),
    ('Numaan Ashraf', 'numaan@makeystreet.com'),
)

# See: https://docs.djangoproject.com/en/dev/ref/settings/#managers
MANAGERS = ADMINS
########## END MANAGER CONFIGURATION


########## DATABASE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.',
        'NAME': '',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}
########## END DATABASE CONFIGURATION


########## GENERAL CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#time-zone
TIME_ZONE = 'America/Los_Angeles'

# See: https://docs.djangoproject.com/en/dev/ref/settings/#language-code
LANGUAGE_CODE = 'en-us'

# See: https://docs.djangoproject.com/en/dev/ref/settings/#site-id
SITE_ID = 1

# See: https://docs.djangoproject.com/en/dev/ref/settings/#use-i18n
USE_I18N = True

# See: https://docs.djangoproject.com/en/dev/ref/settings/#use-l10n
USE_L10N = True

# See: https://docs.djangoproject.com/en/dev/ref/settings/#use-tz
USE_TZ = True
########## END GENERAL CONFIGURATION


########## MEDIA CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#media-root
MEDIA_ROOT = normpath(join(DJANGO_ROOT, 'media'))

# See: https://docs.djangoproject.com/en/dev/ref/settings/#media-url
MEDIA_URL = '/media/'
########## END MEDIA CONFIGURATION


########## STATIC FILE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#static-root
STATIC_ROOT = normpath(join(DJANGO_ROOT, 'static'))

# See: https://docs.djangoproject.com/en/dev/ref/settings/#static-url
STATIC_URL = '/static/'

# See: https://docs.djangoproject.com/en/dev/ref/contrib/
# staticfiles/#std:setting-STATICFILES_DIRS
STATICFILES_DIRS = (
    normpath(join(DJANGO_ROOT, 'assets')),
)

# See: https://docs.djangoproject.com/en/dev/ref/contrib/
# staticfiles/#staticfiles-finders
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)

ADMIN_MEDIA_PREFIX = STATIC_URL + 'admin/'  # must be this value
########## END STATIC FILE CONFIGURATION


########## FIXTURE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/
# settings/#std:setting-FIXTURE_DIRS
FIXTURE_DIRS = (
    normpath(join(DJANGO_ROOT, 'fixtures')),
)
########## END FIXTURE CONFIGURATION


########## TEMPLATE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/
# settings/#template-context-processors

# TEMPLATE_CONTEXT_PROCESSORS = (
#     'django.contrib.auth.context_processors.auth',
#     'django.core.context_processors.debug',
#     'django.core.context_processors.i18n',
#     'django.core.context_processors.media',
#     'django.core.context_processors.static',
#     'django.core.context_processors.tz',
#     'django.contrib.messages.context_processors.messages',
#     'django.core.context_processors.request',
#     # AllAuth context processors
#     'allauth.account.context_processors.account',
#     'allauth.socialaccount.context_processors.socialaccount',
# )

# See: https://docs.djangoproject.com/en/dev/ref/settings/#template-loaders
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

# See: https://docs.djangoproject.com/en/dev/ref/settings/#template-dirs
TEMPLATE_DIRS = (
    normpath(join(DJANGO_ROOT, 'templates')),
)
########## END TEMPLATE CONFIGURATION


########## MIDDLEWARE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#middleware-classes
MIDDLEWARE_CLASSES = (
    # Reversion
    'reversion.middleware.RevisionMiddleware',

    # Domain Redirect Middleware
    'hostname_redirects.middleware.HostnameRedirectMiddleware',
    # Use GZip compression to reduce bandwidth.
    'django.middleware.gzip.GZipMiddleware',

    # Default Django middleware.
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',

    'django.middleware.transaction.TransactionMiddleware',

)
########## END MIDDLEWARE CONFIGURATION


########## URL CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#root-urlconf
ROOT_URLCONF = '%s.urls' % SITE_NAME
########## END URL CONFIGURATION


########## APP CONFIGURATION
DJANGO_APPS = (
    # 'longerusername',

    # Default Django apps:
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.staticfiles',

    #all of these are needed for the askbot
    'django.contrib.admin',
    'django.contrib.humanize',
    'django.contrib.sitemaps',
    'django.contrib.messages',

    # Admin panel and documentation:
    'django.contrib.admindocs',
)

THIRD_PARTY_APPS = (
    # Database migration helpers:
    'south',

    # Static file management:
    'compressor',

    # Asynchronous task queue:
    'djcelery',

    # Open facebook
    'open_facebook',

    # Django Choices
    'dj.choices',

    #ALL AUTH
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.facebook',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.twitter',

    # Django Mandrill
    'djrill',

    # Taggit
    'taggit',

    # Admin Views,
    'adminplus',

    # Reversion
    'reversion',

    #Hijack
    'hijack'
)

LOCAL_APPS = (
    'woot.apps.catalog',
    'woot.apps.core',

    # Hostname Redirects
    'woot.hostname_redirects',
)

# See: https://docs.djangoproject.com/en/dev/ref/settings/#installed-apps
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS
########## END APP CONFIGURATION


########## CELERY CONFIGURATION
# See: http://celery.readthedocs.org/en/latest/
# configuration.html#celery-task-result-expires
CELERY_TASK_RESULT_EXPIRES = timedelta(minutes=30)

# See: http://docs.celeryproject.org/en/master/
# configuration.html#std:setting-CELERY_CHORD_PROPAGATES
CELERY_CHORD_PROPAGATES = True

# See: http://celery.github.com/celery/django/
setup_loader()
########## END CELERY CONFIGURATION


########## WSGI CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#wsgi-application
WSGI_APPLICATION = 'wsgi.application'
########## END WSGI CONFIGURATION


########## COMPRESSION CONFIGURATION
# See: http://django_compressor.readthedocs.org/en/latest/
# settings/#django.conf.settings.COMPRESS_ENABLED
COMPRESS_ENABLED = True

# See: http://django_compressor.readthedocs.org/en/latest/
# settings/#django.conf.settings.COMPRESS_CSS_FILTERS
COMPRESS_CSS_FILTERS = [
    'compressor.filters.template.TemplateFilter',
]

# See: http://django_compressor.readthedocs.org/en/latest/
# settings/#django.conf.settings.COMPRESS_JS_FILTERS
COMPRESS_JS_FILTERS = [
    'compressor.filters.template.TemplateFilter',
]
# COMPRESS_JS_FILTERS = []
########## END COMPRESSION CONFIGURATION

#delayed notifications, time in seconds, 15 mins by default
NOTIFICATION_DELAY_TIME = 60 * 15

#Celery Settings
# BROKER_TRANSPORT = "djkombu.transport.DatabaseTransport"
CELERY_ALWAYS_EAGER = True

# GROUP_MESSAGING = {
#     'BASE_URL_GETTER_FUNCTION': 'askbot.models.user_get_profile_url',
#     'BASE_URL_PARAMS': {'section': 'messages', 'sort': 'inbox'}
# }

# JINJA2_EXTENSIONS = ('compressor.contrib.jinja2ext.CompressorExtension',)

COMPRESS_PRECOMPILERS = (
    ('text/less', 'lessc {infile} {outfile}'),
)
COMPRESS_PARSER = 'compressor.parser.HtmlParser'


RECAPTCHA_USE_SSL = True

CACHE_MIDDLEWARE_ANONYMOUS_ONLY = True

########## TEMPLATE CONTEXT PROCESSOR
TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.request',
    # 'askbot.context.application_settings',
    'django.core.context_processors.i18n',

    # 'askbot.user_messages.context_processors.user_messages',  # must be before
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.csrf',

    'django.core.context_processors.debug',

    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',

    'django.contrib.messages.context_processors.messages',
    # 'django_facebook.context_processors.facebook',
    # AllAuth context processors
    'allauth.account.context_processors.account',
    'allauth.socialaccount.context_processors.socialaccount',

)
########## END TEMPLATE CONTEXT PROCESSOR

########## AUTHENTICATION BACKEND
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    # `allauth` specific authentication methods, such as login by e-mail
    "allauth.account.auth_backends.AuthenticationBackend"
)
########## END AUTHENTICATION BACKEND

########## USER MODEL
# AUTH_USER_MODEL = 'django_facebook.FacebookCustomUser'
########## END USER MODEL


########## SOUTH DISABLE APPS
SOUTH_MIGRATION_MODULES = {
    'taggit': 'taggit.south_migrations',
}
########## END SOUTH DISABLE APPS


########## STATIC BLOB
STATIC_BLOB = 'http://makeystreet.blob.core.windows.net/staticfiles'
########## END STATIC BLOB


########## SECRET CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
SECRET_KEY = r"8uj=)lgfy_6a+)ma(op5b*uo2nccwmsk@#8z+h-=&ieq%e%59z"
########## END SECRET CONFIGURATION

########## Auth And AllAuth settings
LOGIN_URL = '/'
LOGIN_REDIRECT_URL = '/'

ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = "none"
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_LOGOUT_ON_GET = True
ACCOUNT_USERNAME_MIN_LENGTH = 3
ACCOUNT_SIGNUP_FORM_CLASS = 'woot.apps.catalog.forms.SignupForm'
ACCOUNT_USERNAME_BLACKLIST = ['www', 'ns1', 'ns2', 'ns3', 'ns4', 'ns5', 'dns',
                              'http', 'https', 'news', 'nntp', 'ftp', 'sftp',
                              'file', 'mail', 'imap', 'pop3', 'smtp', 'ssh',
                              'tel', 'admin', 'registration', 'register',
                              'about', 'help', 'support', 'staff', 'root',
                              'feed', 'blog', 'noreply', 'media', 'static',
                              'makey', 'maker', 'space', 'article']

ACCOUNT_EMAIL_SUBJECT_PREFIX = "[Makeystreet] "
DEFAULT_FROM_EMAIL = 'Alex J V <alex@makeystreet.com>'

SOCIALACCOUNT_QUERY_EMAIL = True
SOCIALACCOUNT_EMAIL_REQUIRED = True
SOCIALACCOUNT_PROVIDERS = {
    'facebook': {
        'SCOPE': ['public_profile', 'email', 'user_location'],
        'METHOD': 'js_sdk',  # instead of 'oauth2'
        'VERIFIED_EMAIL': True,
    },
    'google': {
        'SCOPE': ['https://www.googleapis.com/auth/userinfo.profile',
                  'https://www.googleapis.com/auth/userinfo.email'],

    }
}
