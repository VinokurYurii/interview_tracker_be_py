import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

@pytest.fixture
def client():
    return APIClient()

@pytest.mark.django_db
def test_login_returns_tokens_with_valid_credentials(client, user):
    url = reverse("token_obtain_pair")
    response = client.post(url, {"email": "alice@example.com", "password": "StrongPass123!"})
    assert response.status_code == status.HTTP_200_OK
    assert "access" in response.data
    assert "refresh" in response.data


@pytest.mark.django_db
def test_login_fails_with_wrong_password(client, user):
    url = reverse("token_obtain_pair")
    response = client.post(url, {"email": "alice@example.com", "password": "wrongpassword"})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

@pytest.mark.django_db
def test_login_fails_with_nonexistent_email(client):
    url = reverse("token_obtain_pair")
    response = client.post(url, {"email": "ghost@example.com", "password": "whatever"})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
