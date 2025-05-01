
from .models import Metal
from .ai import AI_V1
import threading
import time
from django.core.management import call_command

def update_metals():
    while True:
        print("[Thread] Запуск update_metals...")
        call_command('update_metals')
        time.sleep(60*60)  # Интервал в секундах (1 час



def start_scheduler():
    thread = threading.Thread(target=update_metals, daemon=True)
    thread.start()




