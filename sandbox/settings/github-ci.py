from .base import *  # noqa pylint: disable=wildcard-import,unused-wildcard-import

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "wagtail-email-subscription",
        "USER": "postgres",
        "PASSWORD": "postgres",
        "HOST": "localhost",
        "PORT": "5432",
    }
}
