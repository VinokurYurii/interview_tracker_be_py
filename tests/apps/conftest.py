import pytest
from rest_framework.test import APIClient

from apps.users.models import User
from apps.companies.models import Company

@pytest.fixture
def user(db):
    return User.objects.create_user(
        email="alice@example.com",
        password="StrongPass123!",
        first_name="Alice",
        last_name="Smith",
    )


@pytest.fixture
def other_user(db):
    return User.objects.create_user(
        email="bob@example.com",
        password="StrongPass123!",
        first_name="Bob",
        last_name="Jones",
    )


@pytest.fixture
def auth_client(user):
    client = APIClient()
    client.force_authenticate(user=user)
    return client


@pytest.fixture
def company(user):
    return Company.objects.create(user=user, name="Acme")
