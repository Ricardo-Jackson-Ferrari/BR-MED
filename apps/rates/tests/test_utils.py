from datetime import date

import pytest
from rates.utils import (
    get_business_days_in_range,
    validate_start_date_less_than_end_date,
)


class TestValidateStartDateLessThanEndDate:
    def test_valid_range_does_not_raise(self):
        assert not validate_start_date_less_than_end_date(
            date(2025, 6, 1), date(2025, 6, 2)
        )

    def test_invalid_range_raises_value_error(self):
        with pytest.raises(ValueError) as exc_info:
            validate_start_date_less_than_end_date(date(2025, 6, 3), date(2025, 6, 1))
        assert (
            str(exc_info.value) == "A data inicial não pode ser maior que a data final."
        )


class TestGetBusinessDaysInRange:
    def test_range_includes_only_weekdays(self):
        start = date(2025, 6, 2)
        end = date(2025, 6, 6)
        result = get_business_days_in_range(start, end)
        assert result == [
            date(2025, 6, 2),
            date(2025, 6, 3),
            date(2025, 6, 4),
            date(2025, 6, 5),
            date(2025, 6, 6),
        ]

    def test_range_skips_weekends(self):
        start = date(2025, 6, 6)
        end = date(2025, 6, 10)
        result = get_business_days_in_range(start, end)
        assert result == [
            date(2025, 6, 6),
            date(2025, 6, 9),
            date(2025, 6, 10),
        ]

    def test_invalid_range_raises_value_error(self):
        with pytest.raises(ValueError):
            get_business_days_in_range(date(2025, 6, 10), date(2025, 6, 1))
