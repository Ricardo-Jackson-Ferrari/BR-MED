from datetime import date, timedelta
from unittest.mock import Mock, patch

import pytest
from rates.exceptions import RateAPICommunicationError, RateNotFoundError
from rates.models import Currency, Rate
from rates.services.rate_sync_service import RateCaptureService
from rates.services.save_rates import save_rates_to_db


@pytest.mark.django_db
class TestSaveRatesToDB:

    def test_save_new_currencies_and_rates(self):
        data = [
            {
                "date": "2025-06-20",
                "base": "BRL",
                "rates": {
                    "USD": 5.25,
                    "EUR": 5.70,
                },
            }
        ]

        save_rates_to_db(data)

        assert Currency.objects.filter(symbol="BRL").exists()
        assert Currency.objects.filter(symbol="USD").exists()
        assert Currency.objects.filter(symbol="EUR").exists()

        assert Rate.objects.filter(
            base__symbol="BRL",
            target__symbol="USD",
            date="2025-06-20",
            value=5.25,
        ).exists()

        assert Rate.objects.filter(
            base__symbol="BRL",
            target__symbol="EUR",
            date="2025-06-20",
            value=5.70,
        ).exists()

    def test_avoid_duplicate_rates(self):
        brl = Currency.objects.create(symbol="BRL", currency="Real")
        usd = Currency.objects.create(symbol="USD", currency="Dólar")

        Rate.objects.create(
            date="2025-06-21",
            base=brl,
            target=usd,
            value=5.30,
        )

        data = [
            {
                "date": "2025-06-21",
                "base": "BRL",
                "rates": {
                    "USD": 5.30,
                },
            }
        ]

        save_rates_to_db(data)

        assert Rate.objects.count() == 1


class TestRateCaptureService:
    @pytest.fixture
    def mock_adapter(self):
        return Mock()

    @pytest.fixture
    def service(self, mock_adapter):
        return RateCaptureService(adapter=mock_adapter)

    @pytest.fixture
    def business_days(self):
        return [date(2025, 6, 17) + timedelta(days=i) for i in range(5)]

    @patch("rates.services.rate_sync_service.get_business_days_in_range")
    @patch("rates.services.rate_sync_service.save_rates_to_db")
    def test_fetch_rates_success(
        self, save_mock, business_days_mock, service, mock_adapter, business_days
    ):
        business_days_mock.return_value = business_days

        mock_adapter.get_rates_for_date.side_effect = [
            {"date": str(day), "base": "BRL", "rates": {"USD": 5.2}}
            for day in business_days
        ]

        result = service.fetch_rates_for_range(
            start_date=business_days[0],
            end_date=business_days[-1],
            base_currency_symbol="BRL",
            target_currencies_symbols=["USD"],
        )

        assert len(result) == 5
        save_mock.assert_called_once_with(result)

    @patch("rates.services.rate_sync_service.get_business_days_in_range")
    def test_fetch_rates_exceeds_limit(self, business_days_mock, service):
        days = [date(2025, 6, 17) + timedelta(days=i) for i in range(6)]
        business_days_mock.return_value = days

        with pytest.raises(ValueError, match="tem mais do que 5 dias úteis"):
            service.fetch_rates_for_range(days[0], days[-1], "BRL", ["USD"])

    @patch("rates.services.rate_sync_service.get_business_days_in_range")
    def test_fetch_rates_without_rates(self, business_days_mock, service, mock_adapter):
        business_days_mock.return_value = [date(2025, 6, 20)]
        mock_adapter.get_rates_for_date.return_value = {
            "date": "2025-06-20",
            "base": "BRL",
            "rates": {},
        }

        with pytest.raises(RateNotFoundError, match="Nenhuma cotação encontrada"):
            service.fetch_rates_for_range(
                date(2025, 6, 20), date(2025, 6, 20), "BRL", ["USD"]
            )

    @patch("rates.services.rate_sync_service.get_business_days_in_range")
    def test_fetch_rates_api_error(self, business_days_mock, service, mock_adapter):
        business_days_mock.return_value = [date(2025, 6, 20)]
        mock_adapter.get_rates_for_date.side_effect = RateAPICommunicationError(
            "Timeout"
        )

        with pytest.raises(RuntimeError, match="Falha ao se comunicar"):
            service.fetch_rates_for_range(
                date(2025, 6, 20), date(2025, 6, 20), "BRL", ["USD"]
            )

    @patch("rates.services.rate_sync_service.get_business_days_in_range")
    def test_fetch_rates_generic_exception(
        self, business_days_mock, service, mock_adapter
    ):
        business_days_mock.return_value = [date(2025, 6, 20)]
        mock_adapter.get_rates_for_date.side_effect = Exception("Erro desconhecido")

        with pytest.raises(RuntimeError, match="Erro inesperado ao processar"):
            service.fetch_rates_for_range(
                date(2025, 6, 20), date(2025, 6, 20), "BRL", ["USD"]
            )

    @patch("rates.services.rate_sync_service.get_business_days_in_range")
    @patch("rates.services.rate_sync_service.save_rates_to_db")
    def test_fetch_rates_skips_duplicate_dates(
        self, save_mock, business_days_mock, service, mock_adapter
    ):
        business_days_mock.return_value = [date(2025, 6, 19), date(2025, 6, 20)]

        mock_adapter.get_rates_for_date.side_effect = [
            {"date": "2025-06-20", "base": "BRL", "rates": {"USD": 5.2}},
            {"date": "2025-06-20", "base": "BRL", "rates": {"USD": 5.3}},
        ]

        result = service.fetch_rates_for_range(
            start_date=date(2025, 6, 19),
            end_date=date(2025, 6, 20),
            base_currency_symbol="BRL",
            target_currencies_symbols=["USD"],
        )

        # Apenas a primeira deve ser salva
        assert len(result) == 1
        assert result[0]["rates"]["USD"] == 5.2
        save_mock.assert_called_once_with(result)
