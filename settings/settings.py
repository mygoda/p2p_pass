# -*- coding: utf-8 -*-
# __author__ = xutao

from __future__ import division, unicode_literals, print_function
import os
import json
from config import config

DATETIME_FORMAT = "Y-m-d H:i"
SESSION_COOKIE_AGE = 94608000 # cookie三年过期

AUTHENTICATION_BACKENDS = (
    'applications.users.backends.EmailBackend',
    'applications.users.backends.PhoneCheckBackend',
)

LOGIN_URL = "/users/login/"

AUTH_USER_MODEL = "users.User"

PROJECT_HOME = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

DEBUG = True
TEMPLATE_DEBUG = config.getboolean("django", "template_dubug")

# ALLOWED_HOSTS = json.loads(config.get("django", "allowed_hosts"))
ALLOWED_HOSTS = ["*"]
APP_HOST_NAME = config.get("django", "app_host_name")
SYSTEM_NAME = config.get("db", "db_table")

ADMINS = (
    ('Shadow', '18346552658@163.com'),
)

EMAIL_TO = config.get("settings", "email_to")
EMAIL_FROM = config.get("settings", "email_from")

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': config.get("db", "engine"),
        'NAME': config.get("db", "db_table"),
        'USER': config.get("db", "username"),
        'PASSWORD': config.get("db", "password"),
        'HOST': config.get("db", "host"),
        'PORT': '',
    },
}

TIME_ZONE = 'Asia/Shanghai'

LANGUAGE_CODE = 'zh-cn'

SITE_ID = 1

USE_I18N = True

USE_L10N = True

USE_TZ = True

MEDIA_ROOT = os.path.join(PROJECT_HOME, "media")

MEDIA_URL = '/media/'

STATIC_ROOT = os.path.join(PROJECT_HOME, 'static')

STATIC_URL = '/static/'

STATICFILES_DIRS = (
)


STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django.contrib.staticfiles.finders.FileSystemFinder',
)

SECRET_KEY = 'dly31d$+kks@z_!jpie*zw3t=06_as+z(*q8&amp;j0e7p30-euon-'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'raven.contrib.django.raven_compat.middleware.SentryResponseErrorIdMiddleware',
)

ROOT_URLCONF = 'settings.urls'

WSGI_APPLICATION = 'settings.wsgi.application'

TEMPLATE_DIRS = (
    os.path.join(PROJECT_HOME, "templates"),
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.request",
    "django.core.context_processors.i18n",
    'django.contrib.messages.context_processors.messages',
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # third_parts
  #  'debug_toolbar',
    'grappelli.dashboard',
    'grappelli',

    'django.contrib.admin',
    'django.contrib.admindocs',

    'django_extensions',
    "gunicorn",
    'raven.contrib.django.raven_compat',
    'south',
    # apps
    "applications.stat",
    "applications.users",
    "djcelery",

)

# djcelery setting
import djcelery  ###
djcelery.setup_loader()  ###
CELERY_TIMEZONE = 'Asia/Shanghai'  #并没有北京时区，与下面TIME_ZONE应该一致
BROKER_URL = config.get("celery", "BROKER_URL")  #任何可用的redis都可以，不一定要在django server运行的主机上
CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(pathname)s %(lineno)s %(funcName)s %(message)s'
        },
    },
    'filters': {
        'info': {
            '()': 'libs.logs.InfoLevelFilter',
        },
        'warning': {
            '()': 'libs.logs.WarningLevelFilter'
        }
    },
    'handlers': {
        'sentry': {
            'level': 'ERROR',
            'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
        },
        'rotate_warning': {
            'level': 'WARNING',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': os.path.join(PROJECT_HOME, "data", "logs", "warning.log"),
            'when': 'D',
            'formatter': 'verbose',
            'filters': ['warning', ]
        },
        'rotate_info': {
            'level': 'INFO',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': os.path.join(PROJECT_HOME, "data", "logs", "info.log"),
            'when': 'D',
            'formatter': 'verbose',
            'filters': ['info', ]
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        }
    },
    'loggers': {
        '': {
            'level': 'DEBUG',
            'handlers': ['console', 'rotate_info', 'rotate_warning', 'sentry'],
            'propagate': False,
        },
        'django': {
            'level': 'ERROR',
            'handlers': ['console', 'rotate_info', 'rotate_warning'],
        },
        'django.request': {
            'level': 'DEBUG',
            'handlers': ['console', 'rotate_info', 'rotate_warning', 'sentry'],
            'propagate': False,
        },
        'applications': {
            'level': 'DEBUG',
            'handlers': ['console', 'rotate_info', 'rotate_warning', 'sentry'],
            'propagate': False,
        },
        "celery_task": {
            'level': 'DEBUG',
            'handlers': ['console', 'rotate_info', 'rotate_warning', 'sentry'],
            'propagate': False,
        }

    },
}

INTERNAL_IPS = ['127.0.0.1']
GRAPPELLI_INDEX_DASHBOARD = 'settings.dashboard.CustomIndexDashboard'
GRAPPELLI_ADMIN_TITLE = u"首都在线运维管理工具"
# IMG_AVAILABLE_HOSTS = ['zoneke-img.b0.upaiyun.com', ]

#qiniu
QINIU_ACCESS_KEY = config.get('qiniu', 'QINIU_ACCESS_KEY')
QINIU_SECRET_KEY = config.get('qiniu', 'QINIU_SECRET_KEY')
QINIU_BUCKET_NAME = config.get('qiniu', 'QINIU_BUCKET_NAME')
QINIU_BUCKET_DOMAIN = config.get('qiniu', 'QINIU_BUCKET_DOMAIN')


# # WEIXIN
# WX_MANGER_STATES = {
#     "NO_CACHE": "applications.weixin.states.NoCacheState",
#     "MENU": "applications.weixin.states.MenuEventState",
#     "SUBSCRIBE": "applications.weixin.states.SubscribeEventState",
# }

#raven
RAVEN_CONFIG = {
    'dsn': config.get("sentry", "dsn"),
    'auto_log_stacks': False,
}

# PINGXX
PINGXX_TEST_KEY = u"sk_test_X9CmvHuv10GKXr90WTvvnjLC"
PINGXX_KEY = u"sk_test_X9CmvHuv10GKXr90WTvvnjLC"


EMAIL_HOST = "mail.yun-idc.com"
EMAIL_HOST_USER = r"cds\cdsservice"
EMAIL_HOST_PASSWORD = "yun-idc.com"
EMAIL_POSTFIX = "yun-idc.com"
EMAIL_PORT = 443
EMAIL_USE_TLS = False
DEFAULT_FROM_EMAIL = 'cdsservice@yun-idc.com'

CORE_API = config.get("core", "api")

