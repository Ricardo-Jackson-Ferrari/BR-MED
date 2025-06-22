class RateAPICommunicationError(Exception):
    """Erro de comunicação com a API externa de cotação."""

    pass


class RateNotFoundError(Exception):
    """Cotação não encontrada para a data e moedas fornecidas."""

    pass
