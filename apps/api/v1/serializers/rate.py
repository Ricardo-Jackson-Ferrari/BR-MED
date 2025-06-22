from rates.models import Currency, Rate
from rest_framework import serializers


class CurrencyNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = ["id", "currency", "symbol"]


class RateSerializer(serializers.ModelSerializer):
    base = CurrencyNestedSerializer()
    target = CurrencyNestedSerializer()

    class Meta:
        model = Rate
        fields = ["id", "date", "base", "target", "value"]
