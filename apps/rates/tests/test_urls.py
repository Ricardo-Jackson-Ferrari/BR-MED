import pytest
from django.test import Client
from django.urls import resolve, reverse
from rates.views import RateChartView


@pytest.mark.django_db
class TestRatesUrls:
    def test_rate_chart_url_resolves_to_correct_view(self):
        resolver = resolve("/rates/chart/")
        assert resolver.func.view_class == RateChartView

    def test_rate_chart_named_url_reverse(self):
        url = reverse("rates:rate_chart")
        assert url == "/rates/chart/"
