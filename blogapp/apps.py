from django.apps import AppConfig


class BlogappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'blogapp'

    def ready(self):
        # Charge les récepteurs de signaux au démarrage de Django
        import blogapp.signals  # noqa: F401
