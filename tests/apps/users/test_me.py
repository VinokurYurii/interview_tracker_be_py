import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

@pytest.mark.django_db
def test_me_returns_user_profile(auth_client, user):
    url = reverse("user-me")
    response = auth_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data["email"] == user.email
    assert "password" not in response.data

@pytest.mark.django_db
def test_me_update_changes_name(auth_client, user):
    url = reverse("user-me")
    response = auth_client.patch(url, {"first_name": "Alicia"})
    assert response.status_code == status.HTTP_200_OK
    user.refresh_from_db()
    assert user.first_name == "Alicia"

@pytest.mark.django_db
def test_me_unauthenticated_returns_401():
    client = APIClient()
    url = reverse("user-me")
    response = client.get(url)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
