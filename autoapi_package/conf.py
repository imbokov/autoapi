from django.conf import settings

from .constants import SETTINGS_KEY

autoapi_settings: dict = getattr(settings, SETTINGS_KEY, {})
