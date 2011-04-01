# Django settings for georegistry_web project.
import os, sys

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATABASES = {
    'default': {
        'ENGINE': 'sqlite3', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'db',                      # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'UTC'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True


# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
#MEDIA_URL = 'http://b4b.s3.amazonaws.com/media/'
#http://physique7.s3.amazonaws.com/
MEDIA_URL = 'http://127.0.0.1:8000/site_media/'



MEDIASYNC = {
    'BACKEND': 'mediasync.backends.s3',
    'AWS_KEY': "125PVS8477V1GR75H202",
    'AWS_SECRET': "FvZLqApBXmlBw9QUcizgyLaDJRtVm3YZTPkkjOJm",
    'AWS_BUCKET': "physique7",
}
MEDIASYNC['SERVE_REMOTE'] = False


# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/'
ADMIN_MEDIA_PREFIX = 'http://videntitystatic.s3.amazonaws.com/admin/media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = '^raoqm_qssw9fe&^rypocer5m@6dif2jfey^yr@64be*3c+1ym'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)


AUTH_PROFILE_MODULE = 'accounts.UserProfile'

AUTHENTICATION_BACKENDS = ('georegistry_web.accounts.auth.HTTPAuthBackend',
                           'georegistry_web.accounts.auth.EmailBackend',
                           'django.contrib.auth.backends.ModelBackend',
                           )

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.doc.XViewMiddleware',
    'django.middleware.csrf.CsrfResponseMiddleware',
)

ROOT_URLCONF = 'georegistry_web.urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(BASE_DIR, 'templates'),
    os.path.join(BASE_DIR, 'web/gmap/templates'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.admin',
    'mediasync',
    'georegistry_web.web.gmap',
    'georegistry_web.web.list',
    'georegistry_web.web.table',
    'georegistry_web.web.browse',
    #'xform_manager',
    # Uncomment the next line to enable admin documentation:
    #'django.contrib.admindocs',
)


#Webhook settings
CREATE_WEBHOOK=True
TX_CREATE_WEBHOOK_URL="http://127.0.0.1:8000/georegistry_web-webhook-receiver/"
TX_WEBHOOK_KEY="f3861af7-2707-453e-a11f-9e04758a7828"



ACCOUNT_ACTIVATION_DAYS = 2
RESTRICT_REG_DOMAIN_TO = None
MIN_PASSWORD_LEN = 8

EMAIL_HOST = 'smtp.bizmail.yahoo.com'
EMAIL_PORT = 587 #25 by default
EMAIL_HOST_USER = '---'
EMAIL_HOST_PASSWORD = '---'

#GR_SERVER_SETTINGS
GR_USER="alan"
GR_PASS="pass"
GR_SERVER="http://127.0.0.1:8000/"
