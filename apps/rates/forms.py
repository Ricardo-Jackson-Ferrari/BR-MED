from django import forms
from django.utils import timezone

from .adapters.vatcomply_adapter import MIN_DATE_VAT_API
from .facade import get_base_currency, get_currency_choices_excluding_base
from .utils import get_business_days_in_range, validate_start_date_less_than_end_date


class RateComparisonForm(forms.Form):
    base = forms.CharField(
        label="Cotação de",
        widget=forms.TextInput(
            attrs={
                "readonly": "readonly",
                "disabled": "true",
                "autocomplete": "off",
            }
        ),
        required=False,
    )
    target = forms.ChoiceField(label="Para")
    start_date = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date"}), label="Data inicial"
    )
    end_date = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date"}), label="Data final"
    )

    def __init__(self, *args, min_date=None, max_date=None, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["base"].initial = (
            get_base_currency().currency if get_base_currency() else ""
        )
        self.fields["target"].choices = get_currency_choices_excluding_base()

        if min_date is None:
            min_date = MIN_DATE_VAT_API
        if max_date is None:
            max_date = timezone.now().date()

        min_date_str = min_date.strftime("%Y-%m-%d")
        max_date_str = max_date.strftime("%Y-%m-%d")

        self.fields["start_date"].widget.attrs.update(
            {
                "min": min_date_str,
                "max": max_date_str,
            }
        )
        self.fields["end_date"].widget.attrs.update(
            {
                "min": min_date_str,
                "max": max_date_str,
            }
        )

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")

        min_date = MIN_DATE_VAT_API
        max_date = timezone.now().date()

        if start_date and (start_date < min_date or start_date > max_date):
            self.add_error(
                "start_date", f"A data deve estar entre {min_date} e {max_date}."
            )

        if end_date and (end_date < min_date or end_date > max_date):
            self.add_error(
                "end_date", f"A data deve estar entre {min_date} e {max_date}."
            )

        if start_date and end_date:
            try:
                validate_start_date_less_than_end_date(start_date, end_date)
            except ValueError as e:
                raise forms.ValidationError(str(e))

            business_days = get_business_days_in_range(start_date, end_date)
            if len(business_days) > 5:
                raise forms.ValidationError(
                    "O intervalo não pode conter mais que 5 dias úteis."
                )


def get_configured_rate_form(data=None):
    min_date = MIN_DATE_VAT_API
    max_date = timezone.now().date()

    return RateComparisonForm(
        data=data,
        min_date=min_date,
        max_date=max_date,
    )
