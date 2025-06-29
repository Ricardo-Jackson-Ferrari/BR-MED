from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("common.urls")),
    path("rates/", include("rates.urls")),
    path("api/", include("api.urls")),
]
