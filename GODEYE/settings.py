"""
Django settings for GODEYE project.

Generated by 'django-admin startproject' using Django 1.11.7.

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
SECRET_KEY = '@f^xv@9at$p9um1t2c-65!6rc-#$@b4cl^u5o=hdyl*f#)9q*n'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'GOD.apps.GodConfig',
    'django_celery_beat',

     
   
     

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'GODEYE.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
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

WSGI_APPLICATION = 'GODEYE.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'PerfectCRM',
#         'USER': 'root',
#         'PASSWORD': '666',
#         'HOST': '127.0.0.1',
#         'PORT': '3306',
#     }
# }

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

# CACHES = {
#     'default': {
#         'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
#         'LOCATION': 'c:/cache',
#     }
# }


LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

#session设置

SESSION_ENGINE = 'django.contrib.sessions.backends.db'  # 引擎（默认）

SESSION_COOKIE_NAME = "sessionid"  # Session的cookie保存在浏览器上时的key，即：sessionid＝随机字符串（默认）
SESSION_COOKIE_PATH = "/"  # Session的cookie保存的路径（默认）

SESSION_COOKIE_DOMAIN = None  # Session的cookie保存的域名（默认）
SESSION_COOKIE_SECURE = False  # 是否Https传输cookie（默认）
SESSION_COOKIE_HTTPONLY = True  # 是否Session的cookie只支持http传输（默认）
SESSION_COOKIE_AGE = 60*30  # Session的cookie失效日期（2周）（默认）
SESSION_EXPIRE_AT_BROWSER_CLOSE = False  # 是否关闭浏览器使得Session过期（默认）
SESSION_SAVE_EVERY_REQUEST = True  # 是否每次请求都保存Session，默认修改之后才保存（默认）



STATIC_URL = '/static/'
STATICFILES_DIRS=(os.path.join(BASE_DIR,"statics"),
                  )

AUTH_USER_MODEL="GOD.UserProfile"

WORKDIR=os.path.join(BASE_DIR,"log/audit/")

RANDOM_DIR=os.path.join(STATICFILES_DIRS[0], 'random_img')

LOGIN_URL='/account/login'


#任务脚本

TACKLE_SCRIPTS=os.path.join(BASE_DIR,"backend/tackle_task.py")
UPLOAD_DIRS=os.path.join(BASE_DIR,'upload')

#for celery

CELERY_BROKER_URL='redis://192.168.31.162'
CELERY_RESULT_BACKEND='redis://192.168.31.162'
CELERYD_MAX_TASKS_PER_CHILD = 3
CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler'


#for email
'''
# 一、POP3收邮件：
# POP3: 110
# POP3 SSL: 995
# 二、IMAP收邮件：
# IMAP: 143
# IMAP SSL: 993
# 三、SMTP发邮件：
# SMTP: 25
# SMTP SSL: 465
# SMTP TLS: 587
'''
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_USE_SSL = True

EMAIL_HOST = 'smtp.126.com'  # 如果是 163 改成 smtp.163.com
EMAIL_PORT = 25
EMAIL_HOST_USER = 'fengchubojue@126.com' # 帐号
EMAIL_HOST_PASSWORD = '123456q'  # 密码
DEFAULT_FROM_EMAIL = 'fengcFhubojue <fengchubojue@126.com>'

