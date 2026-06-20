import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from apps.users.models import User

@pytest.fixture
def client():
    return APIClient()

@pytest.fixture
def existing_user(db):
    return User.objects.create_user(
        email="alice@example.com",
        password="StrongPass123!",
        first_name="Alice",
        last_name="Smith",
    )

@pytest.mark.django_db
def test_login_returns_tokens_with_valid_credentials(client, existing_user):
    url = reverse("token_obtain_pair")
    response = client.post(url, {"email": "alice@example.com", "password": "StrongPass123!"})
    assert response.status_code == status.HTTP_200_OK
    assert "access" in response.data
    assert "refresh" in response.data


@pytest.mark.django_db
def test_login_fails_with_wrong_password(client, existing_user):
    url = reverse("token_obtain_pair")
    response = client.post(url, {"email": "alice@example.com", "password": "wrongpassword"})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

@pytest.mark.django_db
def test_login_fails_with_nonexistent_email(client):
    url = reverse("token_obtain_pair")
    response = client.post(url, {"email": "ghost@example.com", "password": "whatever"})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
