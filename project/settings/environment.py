from os import environ
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

SECRET_KEY = environ.get('SECRET_KEY', 'INSECURE')

DEBUG = True if environ.get('DEBUG') == '1' else False

ALLOWED_HOSTS = []  # type: ignore

ROOT_URLCONF = 'project.urls'

WSGI_APPLICATION = 'project.wsgi.application'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Django Debug Toolbar
INTERNAL_IPS = [
    "127.0.0.1",
]
