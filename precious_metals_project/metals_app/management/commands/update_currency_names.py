from django.core.management.base import BaseCommand
from django.db import transaction
from metals_app.models import MetalPrice
import os


class Command(BaseCommand):
    help = 'Добавляет названия валют из файла currencies.txt в MetalPrice'

    def handle(self, *args, **options):
        # Шаг 1: Чтение файла с валютами
        currencies = {}
        currencies_en = {}
        try:
            base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            file_path = os.path.join(base_dir, 'C:/Users/Maxon/PycharmProjects/metalls_project/precious_metals_project/currencies.txt')
            file_path_en = os.path.join(base_dir, 'C:/Users/Maxon/PycharmProjects/metalls_project/precious_metals_project/currencies_en.txt')

            with open(file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line:
                        code, name = line.split(' - ', 1)
                        currencies[code.strip()] = name.strip()
            with open(file_path_en, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line:
                        code, name = line.split(' - ', 1)
                        currencies_en[code.strip()] = name.strip()

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Ошибка чтения файла: {e}'))
            return

        # Шаг 2: Обновление записей в базе
        updated = 0
        with transaction.atomic():
            for price in MetalPrice.objects.all():
                name = currencies.get(price.currency)
                name_en = currencies_en.get(price.currency)
                if name:
                    price.currency_name = name
                if name_en:
                    price.currency_name_en = name_en
                price.save()
                updated += 1

        self.stdout.write(
            self.style.SUCCESS(f'Обновлено {updated} записей. Не найдено валют: {len(currencies) - updated}')
        )

        # Шаг 3: Экспорт в JSON (опционально)
        from django.core import serializers
        data = serializers.serialize('json', MetalPrice.objects.all())
        with open('metal_prices.json', 'w', encoding='utf-8') as f:
            f.write(data)
