from abc import ABC, abstractmethod
from datetime import date
from typing import Dict, List


class RateAdapter(ABC):
    @abstractmethod
    def get_rates_for_date(
        self,
        target_date: date,
        base_currency_symbol: str = "USD",
        target_currencies_symbols: List[str] = None,
    ) -> Dict:
        """
        Retorna as cotações de uma data específica.
        Exemplo:
        {
            "date": "2025-06-19",
            "base": "USD",
            "rates": {
                "EUR": 0.8712319219376199,
                "JPY": 145.66997734797002,
                "BRL": 5.4915490503572055
            }
        }
        """
        pass
