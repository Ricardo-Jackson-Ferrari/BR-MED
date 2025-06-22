from django.db import IntegrityError, transaction
from rates.models import Currency, Rate


def save_rates_to_db(rate_data_list):
    """
    Salva dados de cotação no banco de dados.
    """
    symbols = set()
    for item in rate_data_list:
        symbols.add(item["base"])
        symbols.update(item["rates"].keys())

    existing_currencies = Currency.objects.in_bulk(field_name="symbol")
    currency_map = {
        symbol: (
            existing_currencies[symbol]
            if symbol in existing_currencies
            else Currency.objects.create(symbol=symbol, currency=symbol)
        )
        for symbol in symbols
    }
    for item in rate_data_list:
        date_str = item["date"]
        base_symbol = item["base"]
        base_currency = currency_map[base_symbol]

        for target_symbol, value in item["rates"].items():
            target_currency = currency_map[target_symbol]

            try:
                with transaction.atomic():
                    Rate.objects.create(
                        date=date_str,
                        base=base_currency,
                        target=target_currency,
                        value=value,
                    )
            except IntegrityError:
                continue  # ignora duplicata
