import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from apps.companies.models import Company
from apps.positions.models import Position
from apps.interview_stages.models import InterviewStage
from apps.feedbacks.models import Feedback


@pytest.fixture
def position(user, company):
    return Position.objects.create(user=user, company=company, title="Dev")


@pytest.fixture
def interview_stage(position):
    return InterviewStage.objects.create(position=position, stage_type="hr")


def feedback_list_url(position, stage):
    return reverse(
        "interview-stage-feedback-list",
        kwargs={"position_pk": position.pk, "interview_stage_pk": stage.pk},
    )


@pytest.mark.django_db
def test_list_returns_feedbacks_for_own_stage(auth_client, position, interview_stage):
    Feedback.objects.create(interview_stage=interview_stage, feedback_type="self_review", content="Went well")

    response = auth_client.get(feedback_list_url(position, interview_stage))

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]["content"] == "Went well"


@pytest.mark.django_db
def test_create_feedback(auth_client, position, interview_stage):
    response = auth_client.post(
        feedback_list_url(position, interview_stage),
        {"feedback_type": "company", "content": "Strong candidate"},
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert Feedback.objects.filter(interview_stage=interview_stage, feedback_type="company").exists()


@pytest.mark.django_db
def test_cannot_access_other_users_stage_feedbacks(user, other_user):
    other_company = Company.objects.create(user=other_user, name="Other Corp")
    other_position = Position.objects.create(user=other_user, company=other_company, title="Manager")
    other_stage = InterviewStage.objects.create(position=other_position, stage_type="hr")
    Feedback.objects.create(interview_stage=other_stage, feedback_type="self_review", content="Private")

    client = APIClient()
    client.force_authenticate(user=user)
    response = client.get(
        reverse(
            "interview-stage-feedback-list",
            kwargs={"position_pk": other_position.pk, "interview_stage_pk": other_stage.pk},
        )
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_unauthenticated_request_returns_401(position, interview_stage):
    client = APIClient()
    response = client.get(feedback_list_url(position, interview_stage))
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
