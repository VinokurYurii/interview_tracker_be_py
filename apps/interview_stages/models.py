from django.db import models

from apps.positions.models import Position

class InterviewStage(models.Model):
    class StageType(models.TextChoices):
        HR = "hr", "HR"
        TECHNICAL = "technical", "Technical"
        CLIENT = "client", "Client"
        OTHER = "other", "Other"

    class Status(models.TextChoices):
        PLANNED = "planned", "Planned"
        COMPLETED = "completed", "Completed"
        CANCELLED = "cancelled", "Cancelled"

    position = models.ForeignKey(
        Position,
        on_delete=models.CASCADE,
        related_name="interview_stages",
    )
    stage_type = models.CharField(max_length=50, choices=StageType.choices,)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PLANNED,)
    scheduled_at = models.DateTimeField(blank=True, null=True)
    calendar_link = models.URLField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ["scheduled_at"]

    def __str__(self):
        return f"{self.stage_type} - {self.position}"
