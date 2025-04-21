from calendar import month

from django.shortcuts import render
from django.http import JsonResponse
# from .models import Metal

from django.http import JsonResponse
from metals_app.models import Metal

def metals_json_view(request):
    metals = Metal.objects.all()
    result = []

    for metal in metals:
        metal_data = {
            'symbol': metal.symbol,
            'name': metal.name,
            'price_today': str(metal.price_today) if metal.price_today else None,
            'price_week_ago': str(metal.price_week_ago) if metal.price_week_ago else None,
            'price_month_days_ago': str(metal.price_month_days_ago) if metal.price_month_days_ago else None,
            'converted_prices': {}
        }

        prices = metal.converted_prices.all()
        for price in prices:
            if price.currency not in metal_data['converted_prices']:
                metal_data['converted_prices'][price.currency] = {}
            metal_data['converted_prices'][price.currency][price.date_type] = str(price.price)

        result.append(metal_data)

    return JsonResponse(result, safe=False)
