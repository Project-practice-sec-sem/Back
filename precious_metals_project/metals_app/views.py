from calendar import month
from django.shortcuts import render
from django.http import JsonResponse
from django.http import JsonResponse
from metals_app.models import Metal
from metals_app.serializers import MetalSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .ai import AI_V1
import os

def metals_json_view(request):
    metals = Metal.objects.all()
    serializer = MetalSerializer(metals, many=True)
    return JsonResponse(serializer.data, safe=False)



def ai_advice_json_view(request):
    metals = Metal.objects.exclude(
        price_today__isnull=True,
        price_week_ago__isnull=True,
        price_month_days_ago__isnull=True
    )

    analysis_data = {
        metal.symbol: {
            "name": metal.name,
            "prices": {
                "today": float(metal.price_today),
                "week_ago": float(metal.price_week_ago),
                "month_days_ago": float(metal.price_month_days_ago)
            }
        }
        for metal in metals
        if all([metal.price_today, metal.price_week_ago, metal.price_month_days_ago])
    }

    analyzer = AI_V1()
    advice_full = analyzer.analyze_metals(analysis_data)

    if not advice_full:
        return JsonResponse({"error": "Не удалось получить анализ"}, status=500)

    parts = advice_full.split('===')
    advice = parts[0].strip() if len(parts) > 0 else ""
    en_advice = parts[1].strip() if len(parts) > 1 else ""

    return JsonResponse({"advice": advice, "en_advice": en_advice})
