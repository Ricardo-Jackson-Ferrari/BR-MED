from datetime import date, timedelta
from typing import List


def validate_start_date_less_than_end_date(start: date, end: date) -> None:
    if start > end:
        raise ValueError("A data inicial não pode ser maior que a data final.")


def get_business_days_in_range(start_date: date, end_date: date) -> List[date]:
    validate_start_date_less_than_end_date(start_date, end_date)

    return [
        start_date + timedelta(days=i)
        for i in range((end_date - start_date).days + 1)
        if (start_date + timedelta(days=i)).weekday() < 5
    ]
