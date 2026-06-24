from rest_framework import mixins, viewsets
from drf_spectacular.utils import extend_schema

from apps.companies.models import Company
from apps.companies.serializers import CompanySerializer

@extend_schema(tags=["Companies"])
class CompanyViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = CompanySerializer
    
    def get_queryset(self):
        return Company.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)