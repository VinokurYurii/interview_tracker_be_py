from rest_framework import serializers

from apps.companies.serializers import CompanySerializer
from apps.companies.models import Company
from apps.positions.models import Position

class PositionSerializer(serializers.ModelSerializer):
    company = CompanySerializer(read_only=True)
    company_id = serializers.PrimaryKeyRelatedField(
        source="company",
        queryset=Company.objects.all(),
        write_only=True,
    )

    class Meta:
        model = Position
        fields = (
            "id",
            "title",
            "description",
            "vacancy_url",
            "status",
            "company_id",
            "company",
        )
