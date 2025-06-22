import pytest
from common.views import IndexView
from django.urls import resolve, reverse


@pytest.mark.django_db
def test_common_index_url_resolves():
    path = reverse("common:index")
    assert path == "/"

    resolved_view = resolve(path)
    assert resolved_view.func.view_class == IndexView
