from http import HTTPStatus

from django.http import JsonResponse
from django.views.generic import View

from .adapters.vatcomply_adapter import VatcomplyAdapter
from .facade import get_base_currency
from .forms import RateComparisonForm
from .services.rate_sync_service import RateCaptureService


class RateChartView(View):
    def get(self, request, *args, **kwargs):
        form = RateComparisonForm(request.GET)
        if form.is_valid():
            try:
                base = get_base_currency().symbol if get_base_currency() else ""
                target = form.cleaned_data["target"]
                start = form.cleaned_data["start_date"]
                end = form.cleaned_data["end_date"]

                service = RateCaptureService(VatcomplyAdapter())
                rates = service.fetch_rates_for_range(start, end, base, [target])
                return JsonResponse(
                    {
                        "chart_dates": [r["date"] for r in rates],
                        "chart_data": [r["rates"][target] for r in rates],
                        "target_currency": target,
                    }
                )
            except Exception as exc:
                return JsonResponse({"errors": str(exc)}, status=HTTPStatus.BAD_REQUEST)
        return JsonResponse({"errors": form.errors}, status=HTTPStatus.BAD_REQUEST)
