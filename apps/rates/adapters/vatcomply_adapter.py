from datetime import date
from typing import List

import requests
from django.conf import settings

from ..exceptions import RateAPICommunicationError
from .interfaces.rate_adapter import RateAdapter

base_symbol: str = settings.BASE_CURRENCY_SYMBOL

MIN_DATE_VAT_API = date(1999, 1, 4)


class VatcomplyAdapter(RateAdapter):
    BASE_URL = "https://api.vatcomply.com/rates"

    def get_rates_for_date(
        self, date: date, base_currency: str = base_symbol, symbols: List[str] = None
    ):
        params = {"base": base_currency, "date": date.isoformat()}
        if symbols:
            params["symbols"] = ",".join(symbols)

        try:
            response = requests.get(self.BASE_URL, params=params, timeout=5)
            response.raise_for_status()
            return response.json()

        except requests.exceptions.Timeout:
            raise RateAPICommunicationError(
                "A API de cotações demorou muito para responder."
            )

        except requests.exceptions.ConnectionError:
            raise RateAPICommunicationError(
                "Não foi possível se conectar à API de cotações."
            )

        except requests.exceptions.HTTPError as http_err:
            raise RateAPICommunicationError(
                f"Erro HTTP ao acessar a API de cotações: {http_err.response.status_code}."
            )

        except requests.exceptions.RequestException as req_err:
            raise RateAPICommunicationError(
                f"Erro inesperado ao acessar a API de cotações: {str(req_err)}"
            )

        except ValueError as parse_err:
            raise ValueError(f"Erro ao interpretar a resposta da API: {str(parse_err)}")
