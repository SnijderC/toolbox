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
    'south',
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


##       DEBUGGING IMPORT ERROR (BUTT UGLY FIX, SORRY)
#######
fbadminid = ''

tweet_templates = {
    'advice'  :'Ik heb zojuist dit advies op de #Toolbox van @bitsoffreedom opgevolgd: "%s"',
    'app'     :'Ik heb zojuist deze tool gevonden op de #Toolbox van @bitsoffreedom: "%s"',
    'tool'    :'Ik heb zojuist deze dienst ontdekt op de #Toolbox van @bitsoffreedom: "%s"',
    'playlist':'Ik heb zojuist deze adviezen op de #Toolbox van @bitsoffreedom opgevolgd: "%s"',
    'index'   :'Check dit overzicht op de #Toolbox van @bitsoffreedom, super handig!',
}

meta_tags = {
    'title'             : "Internetvrijheid Toolbox - Bits of Freedom",
    'twitter'           : {
         'publisher'    : '@bitsoffreedom',
         'author'       : '@bitsoffreedom',
    },
   
    'description'       : 'Internet Vrijheid Toolbox helpt je met adviezen en laat je tools vinden die jouw privacy respecteren.',
    'permalink'         : 'https://toolbox.bof.nl',
    'imagelink'         : 'https://toolbox.bof.nl',  # this needs a picture!
    'sitename'          : 'Internet Vrijheid Toolbox',
    'articletags'       : ['privacy','vrijheid','internet'],
    'facebook.adminid'  : fbadminid,
    'section'           : 'Overzicht',
    'publishedtime'     : '2015-05-05',
    'modifiedtime'      : '2015-05-05',
    'locale'            : 'nl_NL',
    'type'              : 'website',
}

meta_templates = {
    'title'             :'%s',
    'description'       :'%s', 
    'permalink'         :'https://toolbox.bof.nl%s',
}
#######
