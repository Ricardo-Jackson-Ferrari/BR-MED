from django.conf import settings
from rates.models import Currency


def get_currency_by_symbol(symbol: str) -> Currency | None:
    """
    Retorna a instância de Currency com o símbolo fornecido.

    Args:
        symbol (str): O símbolo da moeda (ex: 'USD', 'EUR').

    Returns:
        Currency | None: Instância correspondente ou None se não encontrada.
    """
    return Currency.objects.filter(symbol=symbol).first()


def get_base_currency() -> Currency | None:
    """
    Retorna a moeda base configurada no projeto.

    A moeda base é definida pela configuração `BASE_CURRENCY_SYMBOL` no settings.

    Returns:
        Currency | None: Instância da moeda base ou None se não encontrada.
    """
    return get_currency_by_symbol(settings.BASE_CURRENCY_SYMBOL)


def get_currency_choices_excluding_base() -> list[tuple[str, str]]:
    """
    Retorna uma lista de tuplas com as moedas disponíveis, exceto a moeda base.

    Returns:
        list[tuple[str, str]]: Lista de opções no formato (symbol, currency).
    """
    return [
        (c.symbol, c.currency)
        for c in Currency.objects.exclude(symbol=settings.BASE_CURRENCY_SYMBOL)
    ]
