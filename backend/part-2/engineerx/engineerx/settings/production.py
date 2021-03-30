from .base import *

DEBUG = False

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ['SECRET_KEY']

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = [os.environ['ALLOWED_HOST']]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER': 'postgres',
        'PASSWORD': os.environ['POSTGRES_PASSWORD'],
        'HOST': 'db',
        'PORT': '5432',
    }
}

try:
    from .local import *
except ImportError:
    pass
