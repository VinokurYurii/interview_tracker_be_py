from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from apps.companies.views import CompanyViewSet
from apps.positions.views import PositionViewSet
from apps.interview_stages.views import InterviewStageViewSet
from apps.feedbacks.views import FeedbackViewSet

router = DefaultRouter()
router.register("companies", CompanyViewSet, basename="company")
router.register("positions", PositionViewSet, basename="position")

positions_router = routers.NestedDefaultRouter(router, "positions", lookup="position")
positions_router.register("interview_stages", InterviewStageViewSet, basename="position-interview-stage")

interview_stages_router = routers.NestedDefaultRouter(positions_router, "interview_stages", lookup="interview_stage")
interview_stages_router.register("feedbacks", FeedbackViewSet, basename="interview-stage-feedback")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/schema/swagger-ui/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("api/users/", include("apps.users.urls")),
    path("api/", include(router.urls)),
    path("api/", include(positions_router.urls)),
    path("api/", include(interview_stages_router.urls)),
]
