import os
import requests
from decimal import Decimal, ROUND_HALF_UP
from metals_app.models import Metal, MetalPrice

api_key = os.getenv('CURRENCY_API_URL')


def fetch_currency_rates():
    try:
        response = requests.get(api_key)
        response.raise_for_status()
        data = response.json()
        rates = data.get('rates', {})
        return rates
    except Exception as e:
        print(f"Ошибка при получении курсов валют: {e}")
        return {}

def convert_and_save_all_prices():
    rates = fetch_currency_rates()
    if not rates:
        print("Курсы валют не получены, конвертация отменена.")
        return

    metals = Metal.objects.all()

    for metal in metals:
        # Словарь с ценами USD по типам дат
        usd_prices = {
            'today': metal.price_today,
            'week_ago': metal.price_week_ago,
            'month_days_ago': metal.price_month_days_ago,
        }

        for currency_code, rate in rates.items():
            if currency_code == 'USD':
                continue  # USD не конвертируем

            for date_type, usd_price in usd_prices.items():
                if usd_price is None:
                    continue

                converted_price = (Decimal(usd_price) * Decimal(rate)).quantize(Decimal('0.0001'), rounding=ROUND_HALF_UP)

                MetalPrice.objects.update_or_create(
                    metal=metal,
                    currency=currency_code,
                    date_type=date_type,
                    defaults={'price': converted_price}
                )
