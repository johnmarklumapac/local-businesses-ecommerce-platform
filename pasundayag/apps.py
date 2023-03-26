from django.apps import AppConfig


class PasundayagConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = "pasundayag"

    def ready(self):
        import pasundayag.signals