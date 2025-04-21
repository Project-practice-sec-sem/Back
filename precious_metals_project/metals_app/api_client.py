import os
from django.conf import settings
from metalpriceapi.client import Client

from .management.commands.update_metals import Command
from .models import Metal


def update_metal_prices():
    client = Client(os.getenv('METALPRICEAPI_KEY'))

    try:
        # Получаем данные для основных металлов
        data = client.fetchLive(
            base=os.getenv('BASE_CURRENCY', 'USD'),
            currencies=['XAU', 'XAG', 'XPT', 'XPD']
        )

        # Обновляем базу данных
        for full_symbol, rate in data.get('rates', {}).items():
            # Пример: full_symbol = 'USDXAU', нам нужно 'XAU'
            if full_symbol.startswith('USD'):
                symbol = full_symbol[3:]  # отрезаем 'USD'
            else:
                symbol = full_symbol

            Metal.objects.update_or_create(
                symbol=symbol,
                defaults={
                    'name': Command.get_metal_name(symbol),
                    'price': rate,  # Используйте поле модели, например price_today, если есть
                    'price_change': Command.calculate_price_change(symbol, rate)
                }
            )

    except Exception as e:
        print(f"Ошибка MetalpriceAPI: {e}")
