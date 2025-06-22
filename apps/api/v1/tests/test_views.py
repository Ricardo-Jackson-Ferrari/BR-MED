import pytest
from django.urls import reverse
from rates.models import Currency, Rate
from rest_framework.test import APIClient


@pytest.mark.django_db
def test_rate_list_view_returns_rates():
    base_currency = Currency.objects.create(currency="Real Brasileiro", symbol="BRL")
    target_currency = Currency.objects.create(currency="Dólar Americano", symbol="USD")

    Rate.objects.create(
        base=base_currency, target=target_currency, value=5.25, date="2025-06-21"
    )
    Rate.objects.create(
        base=base_currency, target=target_currency, value=5.30, date="2025-06-22"
    )

    client = APIClient()

    url = reverse("api:v1:rate-history")

    response = client.get(url)

    assert response.status_code == 200
    data = response.json()

    assert "count" in data
    assert "results" in data
    assert isinstance(data["results"], list)

    assert data["count"] == 2
    assert len(data["results"]) == 2

    first_item = data["results"][0]
    assert "base" in first_item
    assert "target" in first_item
    assert "value" in first_item
    assert "date" in first_item
