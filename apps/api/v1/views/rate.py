from rates.models import Rate
from rest_framework import generics

from ..serializers.rate import RateSerializer


class RateListView(generics.ListAPIView):
    queryset = (
        Rate.objects.select_related("base", "target").all().order_by("date", "id")
    )
    serializer_class = RateSerializer
