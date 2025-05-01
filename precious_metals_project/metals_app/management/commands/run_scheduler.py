
from django.core.management.base import BaseCommand
from metals_app.scheduler import start_scheduler
import time

class Command(BaseCommand):
    help = 'Запускает планировщик задач'

    def handle(self, *args, **options):
        start_scheduler()
        try:
            while True:  # Удерживаем процесс
                time.sleep(1)
        except KeyboardInterrupt:
            self.stdout.write("Сервис остановлен")