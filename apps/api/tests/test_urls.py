from django.urls import reverse


def test_named_url_resolution():
    url = reverse("api:v1:rate-history")
    assert url == "/api/v1/rates/"
