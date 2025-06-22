from datetime import date

import pytest
from django.db.utils import IntegrityError
from model_bakery import baker
from rates.models import Currency, Rate


@pytest.mark.django_db
class TestCurrencyModel:

    def test_str_returns_expected(self):
        currency = baker.prepare(Currency, currency="Dólar Americano", symbol="USD")
        assert str(currency) == "[USD] Dólar Americano"

    def test_symbol_unique_constraint(self):
        baker.make(Currency, symbol="USD")
        with pytest.raises(IntegrityError):
            baker.make(Currency, symbol="USD")


@pytest.mark.django_db
class TestRateModel:

    def test_str_returns_expected(self):
        base = baker.make(Currency, currency="Dólar Americano", symbol="USD")
        target = baker.make(Currency, currency="Euro", symbol="EUR")
        rate_value = 5.123456789012345
        rate = baker.prepare(
            Rate, date=date(2025, 1, 1), base=base, target=target, value=rate_value
        )
        expected = f"USD → EUR: {rate_value} (2025-01-01)"
        assert str(rate) == expected

    def test_unique_together_constraint(self):
        base = baker.make(Currency, symbol="USD")
        target = baker.make(Currency, symbol="EUR")
        date_val = date(2025, 1, 1)
        baker.make(Rate, date=date_val, base=base, target=target, value=5)

        with pytest.raises(IntegrityError):
            baker.make(Rate, date=date_val, base=base, target=target, value=6)

    def test_unique_together_allows_different_date(self):
        base = baker.make(Currency, symbol="USD")
        target = baker.make(Currency, symbol="EUR")
        baker.make(Rate, date=date(2025, 1, 1), base=base, target=target, value=5)
        baker.make(Rate, date=date(2025, 1, 2), base=base, target=target, value=6)

    def test_unique_together_allows_different_target(self):
        base = baker.make(Currency, symbol="USD")
        target1 = baker.make(Currency, symbol="EUR")
        target2 = baker.make(Currency, symbol="BRL")
        baker.make(Rate, date=date(2025, 1, 1), base=base, target=target1, value=5)
        baker.make(Rate, date=date(2025, 1, 1), base=base, target=target2, value=6)

    def test_unique_together_allows_different_base(self):
        base1 = baker.make(Currency, symbol="USD")
        base2 = baker.make(Currency, symbol="BRL")
        target = baker.make(Currency, symbol="EUR")
        baker.make(Rate, date=date(2025, 1, 1), base=base1, target=target, value=5)
        baker.make(Rate, date=date(2025, 1, 1), base=base2, target=target, value=6)
