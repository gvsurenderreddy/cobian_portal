from cobian_portal.settings_base import *

DEBUG = True

DB_NAME = "/Users/bds/src/cobian/cobian_portal/db.cobian"
DB_USER = ""
DB_PASSWORD = ""

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.cobian'),
    }
}

STATIC_URL = '/static/'