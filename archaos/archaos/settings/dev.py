from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-g#*3o7tgc(=(g2uobhd-j3nkn59v+gz3m=d2s1ni_b0(liwsq9"

# SECURITY WARNING: define the correct hosts in production!


ALLOWED_HOSTS = ["*"]

if os.environ.get("MODE") == "prod":
    ALLOWED_HOSTS = ["beta.daysbooksandrecords.com", "daysbooksandrecords.com"]

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"


try:
    from .local import *
except ImportError:
    pass
