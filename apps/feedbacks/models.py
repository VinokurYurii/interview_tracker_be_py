from django.db import models

from apps.interview_stages.models import InterviewStage

class Feedback(models.Model):
    class FeedbackType(models.TextChoices):
        SELF_REVIEW = "self_review", "Self Review"
        COMPANY = "company", "Company"

    interview_stage = models.ForeignKey(
        InterviewStage,
        on_delete=models.CASCADE,
        related_name="feedbacks"
    )
    feedback_type = models.CharField(max_length=20, choices=FeedbackType.choices)
    content = models.TextField()

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return f"{self.feedback_type} - {self.interview_stage}"
