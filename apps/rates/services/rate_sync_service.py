import logging
from datetime import date
from typing import Dict, List

from rates.adapters.interfaces.rate_adapter import RateAdapter
from rates.exceptions import RateAPICommunicationError, RateNotFoundError
from rates.utils import get_business_days_in_range

from .save_rates import save_rates_to_db

logger = logging.getLogger(__name__)


class RateCaptureService:
    def __init__(self, adapter: RateAdapter):
        self.adapter = adapter

    def fetch_rates_for_range(
        self,
        start_date: date,
        end_date: date,
        base_currency_symbol: str,
        target_currencies_symbols: List[str] = None,
    ) -> List[Dict]:
        business_days = get_business_days_in_range(start_date, end_date)

        if len(business_days) > 5:
            raise ValueError(
                "O intervalo de datas fornecido tem mais do que 5 dias úteis."
            )

        seen_dates = set()
        rates = []

        for date_item in business_days:
            try:
                daily_rate = self.adapter.get_rates_for_date(
                    date_item, base_currency_symbol, target_currencies_symbols
                )

                if not daily_rate.get("rates"):
                    formatted_date = date_item.strftime("%d/%m/%Y")
                    raise RateNotFoundError(
                        f"Nenhuma cotação encontrada para {base_currency_symbol} -> {target_currencies_symbols} na data {formatted_date}."
                    )

                rate_date_str = str(daily_rate["date"])
                if rate_date_str not in seen_dates:
                    rates.append(daily_rate)
                    seen_dates.add(rate_date_str)

            except RateNotFoundError as e:
                logger.warning(f"[RateNotFoundError] {e}")
                raise e

            except RateAPICommunicationError as e:
                logger.error(
                    f"[RateAPICommunicationError] Falha de comunicação com a API: {e}"
                )
                raise RuntimeError(
                    "Falha ao se comunicar com o serviço de cotações. Tente novamente mais tarde."
                ) from e

            except Exception as e:
                logger.error(f"[Erro desconhecido] Falha ao processar cotação: {e}")
                raise RuntimeError(
                    "Erro inesperado ao processar as cotações. Tente novamente."
                ) from e
        save_rates_to_db(rates)
        return rates
