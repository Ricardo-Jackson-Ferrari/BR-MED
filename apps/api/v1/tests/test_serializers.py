from datetime import date
from decimal import Decimal

import pytest
from api.v1.serializers.rate import CurrencyNestedSerializer, RateSerializer
from rates.models import Currency, Rate


@pytest.mark.django_db
def test_currency_nested_serializer():
    currency = Currency.objects.create(currency="Real Brasileiro", symbol="BRL")

    serializer = CurrencyNestedSerializer(currency)
    data = serializer.data

    assert data["id"] == currency.id
    assert data["currency"] == "Real Brasileiro"
    assert data["symbol"] == "BRL"


@pytest.mark.django_db
def test_rate_serializer():
    base = Currency.objects.create(currency="Real Brasileiro", symbol="BRL")
    target = Currency.objects.create(currency="Dólar Americano", symbol="USD")

    rate = Rate.objects.create(
        base=base, target=target, value=5.25, date=date(2025, 6, 22)
    )

    serializer = RateSerializer(rate)
    data = serializer.data

    assert data["id"] == rate.id
    assert data["date"] == "2025-06-22"
    assert Decimal(data["value"]) == Decimal("5.25")

    assert data["base"]["id"] == base.id
    assert data["base"]["currency"] == "Real Brasileiro"
    assert data["base"]["symbol"] == "BRL"

    assert data["target"]["id"] == target.id
    assert data["target"]["currency"] == "Dólar Americano"
    assert data["target"]["symbol"] == "USD"
