"""Production settings and globals."""


from os import environ
from urlparse import urlparse

# from memcacheify import memcacheify
from postgresify import postgresify
#from S3 import CallingFormat

from boto.s3.connection import OrdinaryCallingFormat

from common import *


########## EMAIL CONFIGURATION
# # See: https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# # See: https://docs.djangoproject.com/en/dev/ref/settings/#email-host
# EMAIL_HOST = environ.get('EMAIL_HOST', 'smtp.gmail.com')

# # See: https://docs.djangoproject.com/en/dev/ref/settings/#email-host-password
# EMAIL_HOST_PASSWORD = environ.get('EMAIL_HOST_PASSWORD', '')

# # See: https://docs.djangoproject.com/en/dev/ref/settings/#email-host-user
# EMAIL_HOST_USER = environ.get('EMAIL_HOST_USER', 'your_email@example.com')

# # See: https://docs.djangoproject.com/en/dev/ref/settings/#email-port
# EMAIL_PORT = environ.get('EMAIL_PORT', 587)

# # See: https://docs.djangoproject.com/en/dev/ref/settings/#email-subject-prefix
# EMAIL_SUBJECT_PREFIX = '[%s] ' % SITE_NAME

# # See: https://docs.djangoproject.com/en/dev/ref/settings/#email-use-tls
# EMAIL_USE_TLS = True

# # See: https://docs.djangoproject.com/en/dev/ref/settings/#server-email
# SERVER_EMAIL = EMAIL_HOST_USER
MANDRILL_API_KEY = environ.get('MANDRILL_APIKEY', '')
########## END EMAIL CONFIGURATION


########## DATABASE CONFIGURATION
if 'RDS_DB_NAME' in environ:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': environ['RDS_DB_NAME'],
            'USER': environ['RDS_USERNAME'],
            'PASSWORD': environ['RDS_PASSWORD'],
            'HOST': environ['RDS_HOSTNAME'],
            'PORT': environ['RDS_PORT'],
        }
    }
else:
    DATABASES = postgresify()
########## END DATABASE CONFIGURATION


########## CACHE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#caches
# CACHES = memcacheify()
# REDIS_URL = urlparse(environ.get('REDISCLOUD_URL', ''))
# CACHES = {
#     'default': {
#         'BACKEND': 'redis_cache.RedisCache',
#         'LOCATION': '%s:%s' % (REDIS_URL.hostname, REDIS_URL.port),
#         'OPTIONS': {
#             'PASSWORD': REDIS_URL.password,
#             'DB': 0,
#         }
#     }
# }
########## END CACHE CONFIGURATION


########## CELERY CONFIGURATION
# See: http://docs.celeryproject.org/en/latest/
# configuration.html#broker-transport
BROKER_TRANSPORT = 'amqplib'

# Set this number to the amount of allowed concurrent connections on your AMQP
# provider, divided by the amount of active workers you have.
#
# For example, if you have the 'Little Lemur' CloudAMQP plan (their free tier),
# they allow 3 concurrent connections. So if you run a single worker, you'd
# want this number to be 3. If you had 3 workers running, you'd lower this
# number to 1, since 3 workers each maintaining one open connection = 3
# connections total.
#
# See: http://docs.celeryproject.org/en/latest/
# configuration.html#broker-pool-limit
BROKER_POOL_LIMIT = 3

# See: http://docs.celeryproject.org/en/latest/
# configuration.html#broker-connection-max-retries
BROKER_CONNECTION_MAX_RETRIES = 0

# See: http://docs.celeryproject.org/en/latest/configuration.html#broker-url
BROKER_URL = environ.get('RABBITMQ_URL') or environ.get('CLOUDAMQP_URL')

# See: http://docs.celeryproject.org/en/latest/
# configuration.html#celery-result-backend
CELERY_RESULT_BACKEND = 'amqp'
########## END CELERY CONFIGURATION


########## STORAGE CONFIGURATION
# See: http://django-storages.readthedocs.org/en/latest/index.html
INSTALLED_APPS += (
    'storages',
)

# See: http://django-storages.readthedocs.org/en/latest/
# backends/amazon-S3.html#settings
STATICFILES_STORAGE = 'storages.backends.s3boto.S3BotoStorage'

# See: http://django-storages.readthedocs.org/en/latest/
# backends/amazon-S3.html#settings
#AWS_CALLING_FORMAT = CallingFormat.SUBDOMAIN
AWS_CALLING_FORMAT = OrdinaryCallingFormat()
AWS_IS_GZIPPED = True
# See: http://django-storages.readthedocs.org/en/latest/
# backends/amazon-S3.html#settings
AWS_ACCESS_KEY_ID = environ.get('AWS_ACCESS_KEY_ID', '')
AWS_SECRET_ACCESS_KEY = environ.get('AWS_SECRET_ACCESS_KEY', '')
AWS_STORAGE_BUCKET_NAME = environ.get('AWS_STORAGE_BUCKET_NAME', '')
AWS_AUTO_CREATE_BUCKET = True
AWS_QUERYSTRING_AUTH = False

# Custom AWS settings for media storage
DEFAULT_FILE_STORAGE = 'woot.apps.core.storages.AwsS3Storage'
AWS_MEDIA_STORAGE_BUCKET_NAME = 'makeymedia'
MEDIA_URL = 'https://s3.amazonaws.com/%s/' % AWS_MEDIA_STORAGE_BUCKET_NAME

# AWS cache settings, don't change unless you know what you're doing:
AWS_EXPIREY = 60 * 60 * 24 * 7
AWS_HEADERS = {
    'Cache-Control': 'max-age=%d, s-maxage=%d, must-revalidate' % (AWS_EXPIREY,
                                                                   AWS_EXPIREY)
}

# See: https://docs.djangoproject.com/en/dev/ref/settings/#static-url
STATIC_URL = 'https://%s.s3.amazonaws.com/' % AWS_STORAGE_BUCKET_NAME
########## END STORAGE CONFIGURATION


########## COMPRESSION CONFIGURATION
# See: http://django_compressor.readthedocs.org/en/latest/
# settings/#django.conf.settings.COMPRESS_OFFLINE
COMPRESS_OFFLINE = True
COMPRESS_ENABLED = True

# See: http://django_compressor.readthedocs.org/en/latest/
# settings/#django.conf.settings.COMPRESS_STORAGE
COMPRESS_STORAGE = STATICFILES_STORAGE


# See: http://django_compressor.readthedocs.org/en/latest/
# settings/#django.conf.settings.COMPRESS_CSS_FILTERS
COMPRESS_CSS_FILTERS += [
    'compressor.filters.cssmin.CSSMinFilter',
]

# See: http://django_compressor.readthedocs.org/en/latest/
# settings/#django.conf.settings.COMPRESS_JS_FILTERS
COMPRESS_JS_FILTERS += [
    'compressor.filters.jsmin.JSMinFilter',
]
########## END COMPRESSION CONFIGURATION

########## SECRET CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
SECRET_KEY = environ.get('SECRET_KEY', SECRET_KEY)
########## END SECRET CONFIGURATION

########## ALLOWED HOSTS CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ['.herokuapp.com', '.makeystreet.com', '.elasticbeanstalk.com', 'localhost', '172.31.20.101']
########## END ALLOWED HOST CONFIGURATION

########## FACEBOOK
FACEBOOK_APP_ID = environ.get('FACEBOOK_APP_ID', '')
FACEBOOK_APP_SECRET = environ.get('FACEBOOK_APP_SECRET', '')
########## END FACEBOOK


########## LOGGING CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#logging
# mongoHq = urlparse(environ.get('MONGOHQ_URL', ''))

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        # 'mongo_login': {
        #     'level': 'DEBUG',
        #     'class': 'log4mongo.handlers.MongoHandler',
        #     'host': mongoHq.hostname,
        #     'port': mongoHq.port,
        #     'database_name': mongoHq.path[1:],
        #     'collection': 'login',
        #     'username': mongoHq.username,
        #     'password': mongoHq.password,
        #     # 'formatter': 'verbose',
        # },
        # 'mongo_all': {
        #     'level': 'DEBUG',
        #     'class': 'log4mongo.handlers.MongoHandler',
        #     'host': mongoHq.hostname,
        #     'port': mongoHq.port,
        #     'database_name': mongoHq.path[1:],
        #     'collection': 'all',
        #     'username': mongoHq.username,
        #     'password': mongoHq.password,
        #     # 'formatter': 'verbose',
        # },
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins', 'console'],
            'level': 'ERROR',
            'propagate': True,
        },
        'woot.apps.catalog': {
            'level': 'DEBUG',
            'handlers': ['console']
            # 'handlers': ['console', 'mongo_all', 'mongo_login']
        }
    },
    'formatters': {
        'verbose': {
            'format': ('%(asctime)s [%(process)d] [%(levelname)s] ' +
                       'pathname=%(pathname)s lineno=%(lineno)s ' +
                       'funcname=%(funcName)s %(message)s'),
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        }
    },
}
########## END LOGGING CONFIGURATION
