import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from apps.companies.models import Company
from apps.positions.models import Position


@pytest.mark.django_db
def test_list_returns_only_own_positions(auth_client, user, other_user, company):
    other_company = Company.objects.create(user=other_user, name="Other Corp")
    Position.objects.create(user=user, company=company, title="Dev")
    Position.objects.create(user=other_user, company=other_company, title="Manager")

    response = auth_client.get(reverse("position-list"))

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]["title"] == "Dev"


@pytest.mark.django_db
def test_create_position(auth_client, user, company):
    response = auth_client.post(
        reverse("position-list"),
        {"title": "Backend Dev", "company_id": company.id},
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert Position.objects.filter(user=user, title="Backend Dev").exists()


@pytest.mark.django_db
def test_unauthenticated_request_returns_401():
    client = APIClient()
    response = client.get(reverse("position-list"))
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
