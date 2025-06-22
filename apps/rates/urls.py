from django.urls import path

from .views import RateChartView

app_name = "rates"

urlpatterns = [
    path("chart/", RateChartView.as_view(), name="rate_chart"),
]
