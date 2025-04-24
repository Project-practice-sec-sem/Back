from django.apps import AppConfig


class MetalsAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'metals_app'

    def ready(self):
        if not hasattr(self, 'scheduler_started'):  # Защита от дублирования
            self.scheduler_started = True
            from .scheduler import start_scheduler
            start_scheduler()
