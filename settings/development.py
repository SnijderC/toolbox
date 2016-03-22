# -*- coding: utf-8 -*-
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))+"/toolbox/"

"""

        DB specific settings

"""

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'toolbox-dev',
        'HOST': 'localhost',
        'USER': 'root',
        'PASSWORD': 'root'
    }
}

"""

        Application specific settings

"""

ALLOWED_HOSTS = ['*']

title = "Internetvrijheid Toolbox - Bits of Freedom"

tweet_templates = {
    'advice': 'Op de #InternetvrijheidToolbox vond ik uitleg over deze tool. Ook aan de slag met je #privacy en #veiligheid online? ',
    'app': 'Op de #InternetvrijheidToolbox kreeg ik dit handige advies. Ook aan de slag met je #privacy en #veiligheid online?',
    'tool': 'De #InternetvrijheidToolbox gaf mij uitleg over deze dienst. Ook aan de slag met je #privacy en #veiligheid online?',
    'playlist': 'Op de #InternetvrijheidToolbox staat dit handige stappenplan. Ook aan de slag met je #privacy en #veiligheid online?',
    'index': 'Check dit overzicht van de #InternetvrijheidToolbox. Ook zelf aan de slag met je #privacy en #veiligheid online?',
}

meta_tags = {
    'title': title,
    'twitter': {
        'publisher': '@bitsoffreedom',
        'author': '@bitsoffreedom',
    },

    'description': 'Internet Vrijheid Toolbox helpt je met adviezen en laat je tools vinden die jouw privacy respecteren.',
    'permalink': 'https://toolbox.bof.nl',
    'imagelink': 'https://toolbox.bof.nl/static/media/social_logo.png?1',
    'sitename': 'Internetvrijheid Toolbox',
    'articletags': ['privacy', 'vrijheid', 'internet'],
    'section': 'Overzicht',
    'publishedtime': '2015-05-05',
    'modifiedtime': '2015-05-05',
    'locale': 'nl_NL',
    'type': 'website',
}

meta_templates = {
    'title': '%s',
    'description': '%s',
    'permalink': 'https://toolbox.bof.nl%s',
}

slugs = {
    'categorie': {'slug': 'categories', 'single': False, 'multiple': True},
    'platform': {'slug': 'platforms', 'single': False, 'multiple': False},
    'licenties': {'slug': 'licenses', 'single': False, 'multiple': False},
    'prijs': {'slug': 'prices', 'single': False, 'multiple': False},
    'formfactor': {'slug': 'formfactors', 'single': False, 'multiple': False},
    'page': {'slug': 'pagenr', 'single': False, 'multiple': False},
    # this
    'adviezen': {'slug': 'advices', 'single': True, 'multiple': False},
    # XOR this
    'tools': {'slug': 'tools', 'single': True, 'multiple': False},
    # XOR this
    'overzicht': {'slug': 'overview', 'single': True, 'multiple': False},
    # XOR this
    'handleiding': {'slug': 'manuals', 'single': True, 'multiple': False},
}


"""

        Django specific settings

"""

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR+'/logs/error.log',
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['file'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}

DEBUG = True
TEMPLATE_DEBUG = True


# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'nl-nl'

TIME_ZONE = 'Europe/Amsterdam'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR + "static/"
MEDIA_ROOT = STATIC_ROOT + "media/"
MEDIA_URL = STATIC_URL + "media/"

"""

        Image uploading/thumnailing/storing

"""
THUMBNAIL_ALIASES = {
    '': {
        'icon_thumb': {'size': (128, 0), 'crop': False},
        'icon': {'size': (256, 0), 'crop': False},
        'inline': {'size': (600, 0), 'crop': False},
    },
}
THUMBNAIL_BASEDIR = "inline/thumbs/"
THUMBNAIL_PRESERVE_EXTENSIONS = True

FILER_ENABLE_PERMISSIONS = False
FILER_IS_PUBLIC_DEFAULT = True
FILER_DEBUG = False
FILER_STORAGES = {
    'public': {
        'main': {
            'ENGINE': 'filer.storage.PublicFileSystemStorage',
            'OPTIONS': {
                'location': MEDIA_ROOT,
                'base_url': MEDIA_URL,
            },
            #'UPLOAD_TO': 'filer.utils.generate_filename.randomized',
            'UPLOAD_TO': 'toolbox.functions.randomized_file',
            'UPLOAD_TO_PREFIX': 'uploaded',
        },
        'thumbnails': {
            'ENGINE': 'filer.storage.PublicFileSystemStorage',
            'OPTIONS': {
                'location': MEDIA_ROOT,
                'base_url': MEDIA_URL,
            },
            'THUMBNAIL_OPTIONS': {
                'base_dir': 'thumbs',
            },
            'UPLOAD_TO': 'toolbox.functions.randomized_file'
        }
    }
}
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # other finders..
)

SECURE_SSL_REDIRECT = False
