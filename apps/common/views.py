from django.views.generic import TemplateView
from rates.forms import get_configured_rate_form


class IndexView(TemplateView):
    template_name = "common/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = get_configured_rate_form()
        return context
