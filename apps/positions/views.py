from rest_framework import viewsets

from apps.positions.models import Position
from apps.positions.serializers import PositionSerializer

class PositionViewSet(viewsets.ModelViewSet):
    serializer_class = PositionSerializer

    def get_queryset(self):
        return (
            Position.objects.filter(user=self.request.user).select_related("company")
        )

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
