import os
from pathlib import Path
from split_settings.tools import include

from dotenv import load_dotenv
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = os.getenv('SECRET_KEY')

DEBUG = True

include(
    'config/database.py',
    'config/middleware.py',
    'config/templates.py',
    'config/internationalization.py',
    'config/cors.py',
    'config/rest.py',
    'config/celery.py',
    'config/apps.py',
    'config/auth.py',
    'config/hosts.py',
)

ROOT_URLCONF = 'pandora_backend.urls'

WSGI_APPLICATION = 'pandora_backend.wsgi.application'

STATIC_URL = '/static/'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'