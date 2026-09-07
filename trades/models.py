from django.contrib.auth.models import User
from django.db import models


class Trade(models.Model):
    DIRECTION_CHOICES = [
        ("LONG", "Long"),
        ("SHORT", "Short"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="trades",
    )

    entry_time = models.DateTimeField()
    exit_time = models.DateTimeField(
        null=True,
        blank=True,
    )

    symbol = models.CharField(
        max_length=20,
    )

    direction = models.CharField(
        max_length=5,
        choices=DIRECTION_CHOICES,
    )

    lots = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    entry_price = models.DecimalField(
        max_digits=15,
        decimal_places=5,
    )

    exit_price = models.DecimalField(
        max_digits=15,
        decimal_places=5,
        null=True,
        blank=True,
    )

    take_profit = models.DecimalField(
        max_digits=15,
        decimal_places=5,
        null=True,
        blank=True,
    )

    stop_loss = models.DecimalField(
        max_digits=15,
        decimal_places=5,
        null=True,
        blank=True,
    )

    pnl = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0,
    )

    fees = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0,
    )

    setup = models.CharField(
        max_length=100,
        blank=True,
    )

    lesson = models.TextField(
        blank=True,
    )

    score = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ["-entry_time"]

    def __str__(self):
        return f"{self.symbol} - {self.direction}"