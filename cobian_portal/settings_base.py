import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'byf9r(s8pal5er4ni8o(40^65qv3c3!cb3$(=wou2yxwix66v$'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

EMAIL_HOST='smtp.webfaction.com'
EMAIL_HOST_USER='brian_mail'
EMAIL_HOST_PASSWORD='Peello0!'
EMAIL_NO_REPLY = 'noreply@cobianusa.com'

BUYER_PARTY_ID = "COBIANAPI"
SELLER_PARTY_ID = "7607032182"

EBRIDGE_LOGIN = "CobianAPI"
EBRIDGE_PASSWORD = "032182"
EBRIDGE_PARTNER = "Cobian Corp"
EBRIDGE_URL = "https://www.ebridgeservices.com/ePortalService.asmx"
EBRIDGE_WSDL = EBRIDGE_URL + "?WSDL"

ALLOWED_HOSTS = []

# Application definition
INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'easy_thumbnails',
    'tagging',
    'api',
    'db',
    'main',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'cobian_portal.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',
                'main.views.sub_domain',
            ],
        },
    },
]

WSGI_APPLICATION = 'cobian_portal.wsgi.application'

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

THUMBNAIL_PROCESSORS = (
    'easy_thumbnails.processors.colorspace',
    'easy_thumbnails.processors.autocrop',
    'easy_thumbnails.processors.scale_and_crop',
    'easy_thumbnails.processors.filters',
)
