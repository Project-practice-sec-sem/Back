from django.contrib import admin
from .models import Metal

@admin.register(Metal)
class MetalAdmin(admin.ModelAdmin):
    list_display = (
        'symbol',
        'name',
        'price_today',
        'price_week_ago',
        'price_month_days_ago',  # заменили price_month_ago на price_month_days_ago
        'updated_at',
    )
    search_fields = ('symbol', 'name')
    list_filter = ('symbol',)
    readonly_fields = ('updated_at',)
