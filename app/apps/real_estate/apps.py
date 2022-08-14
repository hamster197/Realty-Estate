from django.apps import AppConfig


class RealEstateConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app.apps.real_estate'

    def ready(self):
        import app.apps.real_estate.signals

