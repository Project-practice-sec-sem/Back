# Generated by Django 5.2 on 2025-05-14 11:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('metals_app', '0002_metalprice_currency_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='MetalPriceHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('price', models.DecimalField(decimal_places=4, max_digits=20)),
                ('metal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='price_history', to='metals_app.metal')),
            ],
            options={
                'unique_together': {('metal', 'date')},
            },
        ),
    ]
