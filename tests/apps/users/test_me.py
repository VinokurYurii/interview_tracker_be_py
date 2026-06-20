import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from apps.users.models import User

@pytest.fixture
def user(db):
    return User.objects.create_user(
        email="alice@example.com",
        password="StrongPass123!",
        first_name="Alice",
        last_name="Smith",
    )

@pytest.fixture
def auth_client(user):
    client = APIClient()
    client.force_authenticate(user=user)
    return client

@pytest.mark.django_db
def test_me_returns_user_profile(auth_client, user):
    url = reverse("me")
    response = auth_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data["email"] == user.email
    assert "password" not in response.data

@pytest.mark.django_db
def test_me_update_changes_name(auth_client, user):
    url = reverse("me")
    response = auth_client.patch(url, {"first_name": "Alicia"})
    assert response.status_code == status.HTTP_200_OK
    user.refresh_from_db()
    assert user.first_name == "Alicia"

@pytest.mark.django_db
def test_me_unauthenticated_returns_401():
    client = APIClient()
    url = reverse("me")
    response = client.get(url)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
