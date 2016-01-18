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

EMAIL_ORDERS = ['brian.d.severson@gmail.com', 'brian@appfirst.com']

URL_BASE = ""

MEDIA_ROOT = "/Users/bds/src/cobian/cobian_portal/media/"
MEDIA_URL = "/media/"

STATIC_ROOT = "/Users/bds/src/cobian/cobian_portal/static/"
STATIC_FILES_ROOT = "/Users/bds/src/cobian/cobian_portal/main/static/"
STATIC_URL = '/static/'

PRODUCT_IMAGES_ROOT = BASE_DIR + 'media/products/'

ORDER_URL = "/Users/bds/src/cobian/cobian_portal/static/"
EMAIL_MEDIA_URL = URL_BASE + MEDIA_URL
EMAIL_STATIC_URL = URL_BASE + STATIC_URL
