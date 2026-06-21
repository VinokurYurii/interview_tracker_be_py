from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from apps.feedbacks.models import Feedback
from apps.feedbacks.serializers import FeedbackSerializer
from apps.interview_stages.models import InterviewStage

class FeedbackViewSet(viewsets.ModelViewSet):
    serializer_class = FeedbackSerializer
    permission_classes = [IsAuthenticated]

    def get_interview_stage(self):
        return get_object_or_404(
            InterviewStage,
            pk=self.kwargs["interview_stage_pk"],
            position__user=self.request.user
        )
    
    def get_queryset(self):
        return Feedback.objects.filter(interview_stage=self.get_interview_stage())
    
    def perform_create(self, serializer):
        serializer.save(interview_stage=self.get_interview_stage())
