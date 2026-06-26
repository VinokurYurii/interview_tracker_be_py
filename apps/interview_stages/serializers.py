from rest_framework import serializers

from apps.feedbacks.serializers import FeedbackSerializer
from apps.interview_stages.models import InterviewStage

class InterviewStageSerializer(serializers.ModelSerializer):
    feedbacks = FeedbackSerializer(many=True, read_only=True)

    class Meta:
        model = InterviewStage
        fields = (
            "id",
            "stage_type",
            "status",
            "scheduled_at",
            "calendar_link",
            "notes",
            "position_id",
            "feedbacks",
        )
