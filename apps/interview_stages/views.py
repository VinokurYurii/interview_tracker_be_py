from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema

from apps.interview_stages.models import InterviewStage
from apps.interview_stages.serializers import InterviewStageSerializer
from apps.positions.models import Position
from core.mixins import UnwrapResourceMixin

@extend_schema(tags=["Interview Stages"])
class InterviewStageViewSet(UnwrapResourceMixin, viewsets.ModelViewSet):
    serializer_class = InterviewStageSerializer
    permission_classes = [IsAuthenticated]
    resource_key = "interview_stage"

    def get_position(self):
        if not hasattr(self, "_position"):
            self._position = get_object_or_404(
                Position,
                pk=self.kwargs["position_pk"],
                user=self.request.user
            )
        return self._position

    def get_queryset(self):
        return InterviewStage.objects.filter(position=self.get_position())

    def perform_create(self, serializer):
        serializer.save(position=self.get_position())
