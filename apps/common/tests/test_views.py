from http import HTTPStatus

import pytest
from common import views
from django.urls import resolve, reverse


@pytest.mark.django_db
def test_index_url_resolves():
    path = reverse("common:index")
    resolved = resolve(path)
    assert resolved.view_name == "common:index"
    assert resolved.func.view_class == views.IndexView


@pytest.mark.django_db
def test_index_view_status(client):
    url = reverse("common:index")
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK
