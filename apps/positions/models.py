from django.conf import settings
from django.db import models

from apps.companies.models import Company

class Position(models.Model):
    class Status(models.TextChoices):
        ACTIVE = "active", "Active"
        REJECTED = "rejected", "Rejected"
        OFFER = "offer", "Offer"
        ACCEPTED = "accepted", "Accepted"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="positions",
    )
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="positions",
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    vacancy_url = models.URLField(blank=True, null=True)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.ACTIVE,
    )

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return f"{self.title} at {self.company.name}"