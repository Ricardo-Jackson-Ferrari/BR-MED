import pytest
from model_bakery import baker
from rates import facade
from rates.models import Currency


@pytest.mark.django_db
@pytest.mark.usefixtures("settings")
class TestCurrencyFacade:

    def test_get_currency_by_symbol_found(self):
        currency = baker.make(Currency, symbol="USD")
        result = facade.get_currency_by_symbol("USD")
        assert result == currency

    def test_get_currency_by_symbol_not_found(self, settings):
        result = facade.get_currency_by_symbol("XXX")
        assert result is None

    def test_get_base_currency_found(self, settings):
        base = baker.make(Currency, symbol="USD")
        settings.BASE_CURRENCY_SYMBOL = "USD"
        result = facade.get_base_currency()
        assert result == base

    def test_get_base_currency_not_found(self, settings):
        settings.BASE_CURRENCY_SYMBOL = "ZZZ"
        result = facade.get_base_currency()
        assert result is None

    def test_get_currency_choices_excluding_base(self, settings):
        usd = baker.make(Currency, symbol="USD", currency="Dólar")
        eur = baker.make(Currency, symbol="EUR", currency="Euro")
        jpy = baker.make(Currency, symbol="JPY", currency="Iene")
        settings.BASE_CURRENCY_SYMBOL = "USD"

        choices = facade.get_currency_choices_excluding_base()

        assert (eur.symbol, eur.currency) in choices
        assert (jpy.symbol, jpy.currency) in choices
        assert (usd.symbol, usd.currency) not in choices
        assert len(choices) == 2
