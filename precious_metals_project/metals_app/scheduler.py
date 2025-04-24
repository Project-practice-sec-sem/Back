# import os
# import django
#
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'precious_metals_project.settings')
# django.setup()
# from apscheduler.schedulers.background import BackgroundScheduler
# from django_apscheduler.jobstores import DjangoJobStore, register_events
# from django.core.management import call_command
# import logging
# import datetime
# import time
#
# logger = logging.getLogger(__name__)
#
# # os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'precious_metals_project.settings')
# # django.setup()
#
# def update_metals_job():
#     try:
#         print(f"[{time.ctime()}] Запуск update_metals...")
#         logger.info("🔄 Запуск update_metals...")
#         call_command('update_metals')
#         print(f"[{time.ctime()}] Завершено!")
#         logger.info("✅ Задача update_metals завершена!")
#     except Exception as e:
#         logger.error(f"❌ Ошибка: {str(e)}", exc_info=True)
#
# def file_logger():
#     with open('scheduler_test.log', 'a') as f:
#         f.write(f"[{datetime.datetime.now()}] Работает!\n")
#
#
#
#
# def start():
#     print('запустился start')
#     scheduler = BackgroundScheduler(timezone="UTC")
#     scheduler.add_jobstore(DjangoJobStore(), "default")
#     scheduler.add_job(
#         update_metals_job,
#         'interval',
#         minutes=1,
#         name='Update metals every hour',
#         replace_existing=True,
#     )
#
#     scheduler.add_job(
#         file_logger,
#         'interval',
#         minutes=1,
#         name='File logger'
#     )
#
#     register_events(scheduler)
#     scheduler.start()
#     print("Scheduler started. Press Ctrl+C to exit.")
#
#
#
#
# if __name__ == "__main__":
#     start()
#     import time
#     try:
#         while True:
#             time.sleep(60)
#     except (KeyboardInterrupt, SystemExit):
#         print("Scheduler stopped.")



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




