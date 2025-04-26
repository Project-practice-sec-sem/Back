from rest_framework import serializers
from metals_app.models import Metal


class MetalSerializer(serializers.ModelSerializer):
    converted_prices = serializers.SerializerMethodField()

    class Meta:
        model = Metal
        fields = [
            'symbol',
            'name',
            'price_today',
            'price_week_ago',
            'price_month_days_ago',
            'updated_at',
            'converted_prices'
        ]

    def get_converted_prices(self, obj):
        result = {}
        prices = obj.converted_prices.all()
        for price in prices:
            if price.currency not in result:
                result[price.currency] = {
                'currency_name': price.currency_name,
                'today': None,
                'week_ago': None,
                'month_days_ago': None
            }
            result[price.currency][price.date_type] = str(price.price)
        return result