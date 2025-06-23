import os
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from metalpriceapi.client import Client
from metals_app.models import Metal, MetalPriceHistory
from .receiving_conversion import convert_and_save_all_prices

class Command(BaseCommand):
    help = 'Обновление курсов металлов (сегодня/неделя/3 дня назад)'

    def handle(self, *args, **options):
        api_key = os.getenv('METALPRICEAPI_KEY')
        client = Client(api_key)
        base_currency = 'USD'
        metals = ['XAU', 'XAG', 'XPT', 'XPD']

        # Даты для запросов
        today = datetime.now().date()
        week_ago = today - timedelta(days=7)
        month_days_ago = today - timedelta(days=29)  # заменили месяц на 3 дня

        for symbol in metals:
            try:
                # Текущая цена
                live_data = client.fetchLive(base=base_currency, currencies=[symbol])
                print(f"Ответ live_data для {symbol}:", live_data)
                price_today = str(float(live_data.get('rates', {}).get(f'USD{symbol}')) / 28.35)
                if price_today is None:
                    self.stdout.write(self.style.ERROR(f"Нет данных 'rates' для USD{symbol} в live_data: {live_data}"))
                    continue

                # Цена за неделю
                historical_week = client.fetchHistorical(
                    date=week_ago.strftime('%Y-%m-%d'),
                    base=base_currency,
                    currencies=[symbol]
                )
                print(f"Ответ historical_week для {symbol}:", historical_week)
                price_week_ago = str(float(historical_week.get('rates', {}).get(f'USD{symbol}')) / 28.35)
                if price_week_ago is None:
                    self.stdout.write(self.style.WARNING(f"Нет данных 'rates' для USD{symbol} в historical_week: {historical_week}"))

                # Цена за 3 дня назад (вместо месяца)
                historical_month_days = client.fetchHistorical(
                    date=month_days_ago.strftime('%Y-%m-%d'),
                    base=base_currency,
                    currencies=[symbol]
                )
                print(f"Ответ historical_month_days для {symbol}:", historical_month_days)
                price_month_days_ago = str(float(historical_month_days.get('rates', {}).get(f'USD{symbol}')) / 28.35)
                if price_month_days_ago is None:
                    self.stdout.write(self.style.WARNING(f"Нет данных 'rates' для USD{symbol} в historical_month_days: {historical_month_days}"))

                # Обновление или создание записи
                metal, created = Metal.objects.update_or_create(
                    symbol=symbol,
                    defaults={
                        'name': self.get_metal_name(symbol),
                        'price_today': price_today,
                        'price_week_ago': price_week_ago,
                        'price_month_days_ago': price_month_days_ago
                    }
                )
                # Сохраняем историю за 7 дней в USD
                self.save_price_history(client, metal, today)


            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Ошибка для {symbol}: {str(e)}'))

        self.stdout.write("Обновление конвертированных цен...")
        convert_and_save_all_prices()

        self.stdout.write(self.style.SUCCESS('✅ Данные обновлены!'))

    def save_price_history(self, client, metal, today):
        for i in range(1, 8):  # с 1 по 7 день назад, исключая сегодня (0)
            date = today - timedelta(days=i)
            response = client.fetchHistorical(
                date=date.strftime('%Y-%m-%d'),
                base='USD',
                currencies=[metal.symbol]
            )
            raw_price = response.get('rates', {}).get(f'USD{metal.symbol}')
            if raw_price is None:
                print(f"Нет данных для {metal.symbol} на {date}")
                continue
            price = float(raw_price) / 28.35
            MetalPriceHistory.objects.update_or_create(
                metal=metal,
                date=date,
                defaults={'price': price}
            )


    def get_metal_name(self, symbol):
        names = {
            'XAU': 'Золото',
            'XAG': 'Серебро',
            'XPT': 'Платина',
            'XPD': 'Палладий'
        }
        return names.get(symbol, symbol)

    def calculate_price_change(symbol, current_price):
        last_entry = Metal.objects.filter(symbol=symbol).order_by('-id').first()
        if last_entry and last_entry.price:
            return round(current_price - float(last_entry.price), 4)
        return 0.0







