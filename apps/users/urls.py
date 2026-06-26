from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from apps.users.views import RegisterView, SignOutView, SignInView

urlpatterns = [
    path("sign_up", RegisterView.as_view(), name="sign_up"),
    path("sign_in", SignInView.as_view(), name="sign_in"),
    path("sign_out", SignOutView.as_view(), name="sign_out"),
    path("token/refresh", TokenRefreshView.as_view(), name="token_refresh"),
]
