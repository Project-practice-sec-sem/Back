from rest_framework import serializers
from metals_app.models import Metal


class MetalSerializer(serializers.ModelSerializer):
    converted_prices = serializers.SerializerMethodField()
    history = serializers.SerializerMethodField()

    class Meta:
        model = Metal
        fields = [
            'symbol',
            'name',
            'price_today',
            'price_week_ago',
            'price_month_days_ago',
            'updated_at',
            'converted_prices',
            'history',
        ]

    def get_converted_prices(self, obj):
        result = {}
        prices = obj.converted_prices.all()
        for price in prices:
            if price.currency not in result:
                result[price.currency] = {
                'currency_name': price.currency_name,
                'currency_name_en': price.currency_name_en,
                'today': None,
                'week_ago': None,
                'month_days_ago': None
            }
            result[price.currency][price.date_type] = str(price.price)
        return result

    def get_history(self, obj):
        history_qs = obj.price_history.order_by('date')
        return [
            {
                'date': h.date.isoformat(),
                'price': h.price
            }
            for h in history_qs
        ]