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
    advice = analyzer.analyze_metals(analysis_data)

    if not advice:
        return JsonResponse({"error": "Не удалось получить анализ"}, status=500)

    return JsonResponse({"advice": advice})
