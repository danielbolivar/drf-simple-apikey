from django.apps import AppConfig


class RotationConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "drf_apikey.rotation"
    label = "drf_apikey_rotation"
