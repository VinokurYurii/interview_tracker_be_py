from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema

from apps.positions.models import Position
from apps.positions.serializers import PositionSerializer

@extend_schema(tags=["Positions"])
class PositionViewSet(viewsets.ModelViewSet):
    serializer_class = PositionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return (
            Position.objects.filter(user=self.request.user).select_related("company")
        )

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
