from django.conf import settings
from django.test.signals import setting_changed
from django.utils.text import format_lazy
from django.utils.translation import gettext_lazy as _
from rest_framework.settings import APISettings as _APISettings

USER_SETTINGS = getattr(settings, "SIMPLE_API_KEY", None)

DEFAULTS = {
    "FERNET_SECRET": "",
    "API_KEY_LIFETIME": 365,
    "AUTHENTICATION_MODEL": settings.AUTH_USER_MODEL,
    "AUTHENTICATION_KEYWORD_HEADER": "Api-Key",
}

REMOVED_SETTINGS = ()


class PackageSettings(_APISettings):
    def __check_user_settings(self, user_settings):
        SETTINGS_DOC = "https://django-rest-framework-simple-apikey.readthedocs.io/en/latest/settings.html"

        for setting in REMOVED_SETTINGS:
            if setting in user_settings:
                raise RuntimeError(
                    format_lazy(
                        _(
                            "The '{}' setting has been removed. Please refer to '{}' for available settings."
                        ),
                        setting,
                        SETTINGS_DOC,
                    )
                )

        return user_settings


package_settings = PackageSettings(USER_SETTINGS, DEFAULTS)


def reload_api_settings(*args, **kwargs):
    global package_settings

    setting, value = kwargs["setting"], kwargs["value"]

    if setting == "SIMPLE_API_KEY":
        package_settings = PackageSettings(value, DEFAULTS)


setting_changed.connect(reload_api_settings)