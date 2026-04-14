from .base import *
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

DEBUG = False

ALLOWED_HOSTS = [
    BACKEND_SITE_HOST,
    "localhost",
    ".vercel.app",
    "127.0.0.1"
]

CSRF_TRUSTED_ORIGINS = [
    "https://readers-publications-server.vercel.app",
]


# Static variables
STATIC_URL = '/static/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"