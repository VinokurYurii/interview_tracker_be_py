from rest_framework import serializers

from apps.interview_stages.models import InterviewStage

class InterviewStageSerializer(serializers.ModelSerializer):
    class Meta:
        model = InterviewStage
        fields = (
            "id",
            "stage_type",
            "status",
            "scheduled_at",
            "calendar_link",
            "notes",
        )
