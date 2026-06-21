from rest_framework import mixins, viewsets

from apps.companies.models import Company
from apps.companies.serializers import CompanySerializer

class CompanyViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = CompanySerializer
    
    def get_queryset(self):
        return Company.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)