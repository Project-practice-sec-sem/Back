from calendar import month

from django.shortcuts import render
from django.http import JsonResponse
# from .models import Metal

from django.http import JsonResponse
from metals_app.models import Metal
from metals_app.serializers import MetalSerializer

def metals_json_view(request):
    metals = Metal.objects.all()
    serializer = MetalSerializer(metals, many=True)
    return JsonResponse(serializer.data, safe=False)
