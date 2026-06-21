import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from apps.companies.models import Company


@pytest.mark.django_db
def test_list_returns_only_own_companies(auth_client, user, other_user):
    Company.objects.create(user=user, name="My Company")
    Company.objects.create(user=other_user, name="Other Company")

    response = auth_client.get(reverse("company-list"))

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]["name"] == "My Company"


@pytest.mark.django_db
def test_create_company(auth_client, user):
    response = auth_client.post(reverse("company-list"), {"name": "New Company"})

    assert response.status_code == status.HTTP_201_CREATED
    assert Company.objects.filter(user=user, name="New Company").exists()


@pytest.mark.django_db
def test_unauthenticated_request_returns_401():
    client = APIClient()
    response = client.get(reverse("company-list"))
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
