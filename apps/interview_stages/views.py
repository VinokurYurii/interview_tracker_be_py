from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from apps.interview_stages.models import InterviewStage
from apps.interview_stages.serializers import InterviewStageSerializer
from apps.positions.models import Position

class InterviewStageViewSet(viewsets.ModelViewSet):
    serializer_class = InterviewStageSerializer
    permission_classes = [IsAuthenticated]

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
