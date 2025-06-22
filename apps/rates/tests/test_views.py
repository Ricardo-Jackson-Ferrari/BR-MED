from datetime import date
from unittest.mock import MagicMock, patch

import pytest
from django.test import Client
from django.urls import reverse
from rates.models import Currency


@pytest.mark.django_db
class TestRateChartView:
    def setup_method(self):
        self.client = Client()
        self.brl = Currency.objects.create(currency="Real Brasileiro", symbol="BRL")
        self.usd = Currency.objects.create(currency="Dólar Americano", symbol="USD")

    @patch("rates.views.RateCaptureService")
    def test_get_valid_data_returns_chart(self, mock_rate_capture_service, settings):
        settings.BASE_CURRENCY_SYMBOL = self.brl.symbol

        mock_rate_capture_service_instance = mock_rate_capture_service.return_value
        mock_rate_capture_service_instance.fetch_rates_for_range.return_value = [
            {"date": "2025-06-01", "rates": {"USD": 5.10}},
            {"date": "2025-06-02", "rates": {"USD": 5.15}},
        ]

        url = reverse("rates:rate_chart")
        data = {
            "target": "USD",
            "start_date": "2025-06-01",
            "end_date": "2025-06-02",
        }

        response = self.client.get(url, data)
        assert response.status_code == 200

        json_data = response.json()
        assert json_data["chart_dates"] == ["2025-06-01", "2025-06-02"]
        assert json_data["chart_data"] == [5.10, 5.15]
        assert json_data["target_currency"] == "USD"

    def test_get_invalid_form_returns_errors(self):
        url = reverse("rates:rate_chart")
        data = {
            "target": "",
            "start_date": "2025-06-01",
            "end_date": "2025-06-02",
        }
        response = self.client.get(url, data)
        assert response.status_code == 400
        json_data = response.json()
        assert "target" in json_data["errors"]

    @patch("rates.views.RateCaptureService")
    def test_service_raises_exception_returns_400(
        self, mock_rate_capture_service, settings
    ):
        settings.BASE_CURRENCY_SYMBOL = self.brl.symbol
        mock_rate_capture_service_instance = mock_rate_capture_service.return_value
        mock_rate_capture_service_instance.fetch_rates_for_range.side_effect = (
            Exception("Erro de serviço")
        )

        url = reverse("rates:rate_chart")
        data = {
            "target": "USD",
            "start_date": "2025-06-01",
            "end_date": "2025-06-02",
        }
        response = self.client.get(url, data)
        assert response.status_code == 400
        json_data = response.json()
        assert "Erro de serviço" in json_data["errors"]
