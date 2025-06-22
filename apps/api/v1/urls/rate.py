from django.urls import path

from ..views.rate import RateListView

app_name = "v1"

urlpatterns = [
    path("rates/", RateListView.as_view(), name="rate-history"),
]
