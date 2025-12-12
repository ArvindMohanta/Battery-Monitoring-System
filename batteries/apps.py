from django.apps import AppConfig


class BatteriesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'batteries'
    verbose_name = 'Battery Management'
    
    def ready(self):
        # Import signal handlers to ensure they are registered
        try:
            from . import signals  # noqa: F401
        except Exception:
            pass
