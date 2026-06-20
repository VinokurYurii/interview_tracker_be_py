import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

@pytest.fixture
def client():
    return APIClient()

@pytest.mark.django_db
def test_register_returns_201_with_valid_data(client):
    url = reverse("register")
    payload = {
        "email": "alice@example.com",
        "password": "StrongPass123!",
        "first_name": "Alice",
        "last_name": "Smith",
    }
    response = client.post(url, payload)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["email"] == "alice@example.com"
    assert "password" not in response.data

@pytest.mark.django_db
def test_register_fails_with_duplicate_email(client):
    url = reverse("register")
    payload = {
        "email": "alice@example.com",
        "password": "StrongPass123!",
        "first_name": "Alice",
        "last_name": "Smith",
    }
    client.post(url, payload)
    response = client.post(url, payload)
    assert response.status_code == status.HTTP_400_BAD_REQUEST

@pytest.mark.django_db
def test_register_fails_with_weak_password(client):
    url = reverse("register")
    payload = {
        "email": "bob@example.com",
        "password": "123",
        "first_name": "Bob",
        "last_name": "Jones",
    }
    response = client.post(url, payload)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
