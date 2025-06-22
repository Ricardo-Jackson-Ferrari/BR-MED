from datetime import date
from unittest.mock import Mock, patch

import pytest
import requests
from rates.adapters.vatcomply_adapter import VatcomplyAdapter
from rates.exceptions import RateAPICommunicationError


@pytest.fixture
def adapter():
    return VatcomplyAdapter()


@pytest.fixture
def sample_response():
    return {
        "date": "2025-06-22",
        "base": "BRL",
        "rates": {"USD": 5.23, "EUR": 6.12},
    }


@patch("rates.adapters.vatcomply_adapter.requests.get")
def test_get_rates_for_date_success(mock_get, adapter, sample_response):
    mock_response = Mock()
    mock_response.raise_for_status.return_value = None
    mock_response.json.return_value = sample_response
    mock_get.return_value = mock_response

    result = adapter.get_rates_for_date(
        date(2025, 6, 22), base_currency="BRL", symbols=["USD", "EUR"]
    )
    assert result == sample_response
    mock_get.assert_called_once()
    assert mock_get.call_args[1]["params"]["symbols"] == "USD,EUR"


@patch("rates.adapters.vatcomply_adapter.requests.get")
def test_get_rates_for_date_without_symbols(mock_get, adapter, sample_response):
    mock_response = Mock()
    mock_response.raise_for_status.return_value = None
    mock_response.json.return_value = sample_response
    mock_get.return_value = mock_response

    result = adapter.get_rates_for_date(date(2025, 6, 22), base_currency="BRL")
    assert result == sample_response
    assert "symbols" not in mock_get.call_args[1]["params"]


@patch(
    "rates.adapters.vatcomply_adapter.requests.get",
    side_effect=requests.exceptions.Timeout,
)
def test_get_rates_timeout(mock_get, adapter):
    with pytest.raises(RateAPICommunicationError, match="demorou muito para responder"):
        adapter.get_rates_for_date(date.today(), "BRL", ["USD"])


@patch(
    "rates.adapters.vatcomply_adapter.requests.get",
    side_effect=requests.exceptions.ConnectionError,
)
def test_get_rates_connection_error(mock_get, adapter):
    with pytest.raises(RateAPICommunicationError, match="conectar à API"):
        adapter.get_rates_for_date(date.today(), "BRL", ["USD"])


@patch("rates.adapters.vatcomply_adapter.requests.get")
def test_get_rates_http_error(mock_get, adapter):
    mock_response = Mock()
    mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError(
        response=Mock(status_code=404)
    )
    mock_get.return_value = mock_response

    with pytest.raises(RateAPICommunicationError, match="Erro HTTP.*404"):
        adapter.get_rates_for_date(date.today(), "BRL", ["USD"])


@patch(
    "rates.adapters.vatcomply_adapter.requests.get",
    side_effect=requests.exceptions.RequestException("Erro genérico"),
)
def test_get_rates_generic_request_exception(mock_get, adapter):
    with pytest.raises(RateAPICommunicationError, match="Erro inesperado"):
        adapter.get_rates_for_date(date.today(), "BRL", ["USD"])


@patch("rates.adapters.vatcomply_adapter.requests.get")
def test_get_rates_invalid_json(mock_get, adapter):
    mock_response = Mock()
    mock_response.raise_for_status.return_value = None
    mock_response.json.side_effect = ValueError("JSON inválido")
    mock_get.return_value = mock_response

    with pytest.raises(ValueError, match="interpretar a resposta da API"):
        adapter.get_rates_for_date(date.today(), "BRL", ["USD"])
