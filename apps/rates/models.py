from django.db import models


class Currency(models.Model):
    currency = models.CharField(max_length=50)
    symbol = models.CharField(max_length=3, unique=True)

    def __str__(self):
        return f"[{self.symbol}] {self.currency}"


class Rate(models.Model):
    date = models.DateField()
    base = models.ForeignKey(
        Currency, on_delete=models.CASCADE, related_name="base_rates"
    )
    target = models.ForeignKey(
        Currency, on_delete=models.CASCADE, related_name="target_rates"
    )
    value = models.DecimalField(max_digits=20, decimal_places=15)

    class Meta:
        unique_together = ("date", "base", "target")

    def __str__(self):
        return f"{self.base.symbol} → {self.target.symbol}: {self.value} ({self.date})"
