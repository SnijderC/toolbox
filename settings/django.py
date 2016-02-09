"""
Django settings for toolbox project.

NOTE: Most settings have moved to production.py (and development.py)

      " These are not the settings you are looking for " 

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'markdown',
    'pagedown',
    'easy_thumbnails',
    'filer',
    'toolbox'
)

SOUTH_MIGRATION_MODULES = {
        'easy_thumbnails': 'easy_thumbnails.south_migrations',
    }

THUMBNAIL_PROCESSORS = (
    'easy_thumbnails.processors.colorspace',
    #'easy_thumbnails.processors.autocrop',
    'easy_thumbnails.processors.scale_and_crop',
    'easy_thumbnails.processors.filters',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

TEMPLATE_DIRS = (
    BASE_DIR + 'toolbox/templates',
)


TEMPLATE_LOADERS = (
    ('pyjade.ext.django.Loader',(
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    )),
)

ROOT_URLCONF = 'toolbox.app'

WSGI_APPLICATION = 'toolbox.wsgi.application'

# i18n nitty gritty

USE_I18N = True

USE_L10N = True

USE_TZ = True

DEFAULT_CHARSET = "utf-8"

SECRET_KEY          = "9xP7AEHJvXRIESfjOT9NmuXBkhzerW6H"
