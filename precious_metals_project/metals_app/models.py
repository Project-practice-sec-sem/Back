from django.db import models

class Metal(models.Model):
    symbol = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=50)

    # Цены в USD
    price_today = models.DecimalField(max_digits=20, decimal_places=4, null=True, blank=True)
    price_week_ago = models.DecimalField(max_digits=20, decimal_places=4, null=True, blank=True)
    price_month_days_ago = models.DecimalField(max_digits=20, decimal_places=4, null=True, blank=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.symbol})"



class MetalPrice(models.Model):
    metal = models.ForeignKey(Metal, on_delete=models.CASCADE, related_name='converted_prices')
    currency = models.CharField(max_length=10)  # 'EUR', 'RUB', 'GBP', и т.д.
    currency_name = models.CharField(max_length=100, blank=True)
    date_type = models.CharField(max_length=20)  # 'today', 'week_ago', 'month_days_ago'
    price = models.DecimalField(max_digits=20, decimal_places=4)

    class Meta:
        unique_together = ('metal', 'currency', 'date_type')

    def __str__(self):
        return f"{self.metal.symbol} {self.currency} {self.date_type}: {self.price}"

class MetalPriceHistory(models.Model):
    metal = models.ForeignKey(Metal, on_delete=models.CASCADE, related_name='price_history')
    date = models.DateField()
    price = models.DecimalField(max_digits=20, decimal_places=4)

    class Meta:
        unique_together = ('metal', 'date')

    def __str__(self):
        return f"{self.metal.symbol} {self.date}: {self.price}"
