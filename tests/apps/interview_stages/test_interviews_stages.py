import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from apps.companies.models import Company
from apps.positions.models import Position
from apps.interview_stages.models import InterviewStage


@pytest.fixture
def position(user, company):
    return Position.objects.create(user=user, company=company, title="Dev")


@pytest.mark.django_db
def test_list_returns_only_stages_for_own_position(auth_client, position):
    InterviewStage.objects.create(position=position, stage_type="hr")

    response = auth_client.get(
        reverse("position-interview-stage-list", kwargs={"position_pk": position.pk})
    )

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]["stage_type"] == "hr"


@pytest.mark.django_db
def test_create_interview_stage(auth_client, position):
    response = auth_client.post(
        reverse("position-interview-stage-list", kwargs={"position_pk": position.pk}),
        {"stage_type": "technical"},
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert InterviewStage.objects.filter(position=position, stage_type="technical").exists()


@pytest.mark.django_db
def test_cannot_access_other_users_position_stages(user, other_user):
    other_company = Company.objects.create(user=other_user, name="Other Corp")
    other_position = Position.objects.create(user=other_user, company=other_company, title="Manager")
    InterviewStage.objects.create(position=other_position, stage_type="hr")

    client = APIClient()
    client.force_authenticate(user=user)
    response = client.get(
        reverse("position-interview-stage-list", kwargs={"position_pk": other_position.pk})
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_unauthenticated_request_returns_401(position):
    client = APIClient()
    response = client.get(
        reverse("position-interview-stage-list", kwargs={"position_pk": position.pk})
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
