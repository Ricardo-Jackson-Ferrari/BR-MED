from datetime import date, timedelta

import pytest
from django.utils import timezone
from rates.adapters.vatcomply_adapter import MIN_DATE_VAT_API
from rates.forms import RateComparisonForm
from rates.models import Currency


@pytest.mark.django_db
class TestRateComparisonForm:
    def setup_method(self):
        self.brl = Currency.objects.create(currency="Real Brasileiro", symbol="BRL")
        self.usd = Currency.objects.create(currency="Dólar Americano", symbol="USD")
        self.eur = Currency.objects.create(currency="Euro", symbol="EUR")

    def test_base_field_initial(self, settings):
        settings.BASE_CURRENCY_SYMBOL = "BRL"
        form = RateComparisonForm()
        assert form.fields["base"].initial == "Real Brasileiro"

    def test_base_field_empty_if_none(self, settings):
        settings.BASE_CURRENCY_SYMBOL = "XXX"
        form = RateComparisonForm()
        assert form.fields["base"].initial == ""

    def test_target_choices_exclude_base(self, settings):
        settings.BASE_CURRENCY_SYMBOL = "BRL"
        form = RateComparisonForm()
        choices = form.fields["target"].choices
        symbols = [symbol for symbol, _ in choices]
        assert "USD" in symbols
        assert "EUR" in symbols
        assert "BRL" not in symbols

    def test_date_field_attributes(self):
        form = RateComparisonForm()
        min_date = MIN_DATE_VAT_API.strftime("%Y-%m-%d")
        max_date = timezone.now().date().strftime("%Y-%m-%d")

        assert form.fields["start_date"].widget.attrs["min"] == min_date
        assert form.fields["start_date"].widget.attrs["max"] == max_date
        assert form.fields["end_date"].widget.attrs["min"] == min_date
        assert form.fields["end_date"].widget.attrs["max"] == max_date

    def test_valid_data(self):
        today = date.today()
        start = today - timedelta(days=7)
        end = today
        data = {
            "target": "BRL",
            "start_date": str(start),
            "end_date": str(end),
        }
        form = RateComparisonForm(data=data)
        assert form.is_valid()

    def test_missing_target_field(self):
        data = {
            "start_date": str(date.today() - timedelta(days=5)),
            "end_date": str(date.today()),
        }
        form = RateComparisonForm(data=data)
        assert not form.is_valid()
        assert "target" in form.errors

    def test_invalid_date_range_should_fail_if_start_date_after_end_date(self):
        data = {
            "target": "BRL",
            "start_date": "2025-06-10",
            "end_date": "2025-06-01",
        }
        form = RateComparisonForm(data=data)
        assert not form.is_valid()
        assert "A data inicial não pode ser maior que a data final." in str(form.errors)

    def test_more_than_5_business_days_should_fail(self):
        data = {
            "target": "BRL",
            "start_date": "2025-06-10",
            "end_date": "2025-06-18",
        }
        form = RateComparisonForm(data=data)
        assert not form.is_valid()
        assert "O intervalo não pode conter mais que 5 dias úteis." in str(form.errors)

    def test_start_outside_limits_should_fail(self):
        data = {
            "target": "BRL",
            "start_date": "1900-01-01",
            "end_date": str(date.today()),
        }
        form = RateComparisonForm(data=data)
        assert not form.is_valid()
        assert "A data deve estar entre" in str(form.errors)

    def test_end_date_outside_limits_should_fail(self):
        data = {
            "target": "BRL",
            "start_date": str(date.today()),
            "end_date": str(date.today() + timedelta(days=1)),
        }
        form = RateComparisonForm(data=data)
        assert not form.is_valid()
        assert "A data deve estar entre" in str(form.errors)

    def test_clean_does_not_run_if_start_date_missing(self):
        data = {"target": "BRL", "end_date": str(date.today())}
        form = RateComparisonForm(data=data)
        form.is_valid()
        assert "start_date" in form.errors
