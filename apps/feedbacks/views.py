from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema

from apps.feedbacks.models import Feedback
from apps.feedbacks.serializers import FeedbackSerializer
from apps.interview_stages.models import InterviewStage
from core.mixins import UnwrapResourceMixin

@extend_schema(tags=["Feedbacks"])
class FeedbackViewSet(UnwrapResourceMixin, viewsets.ModelViewSet):
    serializer_class = FeedbackSerializer
    permission_classes = [IsAuthenticated]
    resource_key = "feedback"

    def get_interview_stage(self):
        if not hasattr(self, "_interview_stage"):
            self._interview_stage = get_object_or_404(
                InterviewStage,
                pk=self.kwargs["interview_stage_pk"],
                position__user=self.request.user
            )
        return self._interview_stage
    
    def get_queryset(self):
        return Feedback.objects.filter(interview_stage=self.get_interview_stage())
    
    def perform_create(self, serializer):
        serializer.save(interview_stage=self.get_interview_stage())
