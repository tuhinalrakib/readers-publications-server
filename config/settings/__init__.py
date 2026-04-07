from decouple import config

if config("DJANGO_ENV", default="local") == "production":
    from .production import *
else:
    from .development import *
