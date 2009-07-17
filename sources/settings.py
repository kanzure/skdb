# Django settings for sources project.

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Smari McCarthy', 'smari@anarchism.is'),
)

MANAGERS = ADMINS

DATABASE_ENGINE = 'mysql'           # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
DATABASE_NAME = 'sources'             # Or path to database file if using sqlite3.
DATABASE_USER = 'tangiblebit'             # Not used with sqlite3.
DATABASE_PASSWORD = 'goear876snazz'         # Not used with sqlite3.
DATABASE_HOST = ''             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Atlantic/Reykjavik'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = '/home/smari/www/tangiblebit.com/media/'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/media/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/admin/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'tz(yw)bx_c##xki6)oz82910z9i#ihrb5l4xzngr8$i+-^1m6k'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
)

ROOT_URLCONF = 'urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
	"/home/smari/www/tangiblebit.com/sources/templates",
)

INSTALLED_APPS = (
	'django.contrib.auth',
	'django.contrib.admin',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.sites',
	'django.contrib.databrowse',
	'basesite',
	'fjarlog',
	'fabmap',
	'xmlrpc',
)

# import fabmap.xmlrpc

XMLRPC_METHODS = (
        ('sources.fabmap.xmlrpc.getsitelist', 'FabMapGetSites',),
        ('sources.fabmap.xmlrpc.getsitedetails', 'FabMapGetSiteDetails',),
        ('sources.fabmap.xmlrpc.getequipmenttypes', 'FabMapGetEquipmentTypes',),
)
