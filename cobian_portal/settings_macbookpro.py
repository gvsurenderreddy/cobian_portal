from cobian_portal.settings_base import *

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.cobian'),
    }
}

STATIC_URL = '/static/'