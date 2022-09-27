from django.apps import AppConfig


class MysiteConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mySite'
    
    def ready(self):
        import mySite.signals
