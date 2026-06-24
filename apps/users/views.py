from rest_framework import generics, permissions
from drf_spectacular.utils import extend_schema

from apps.users.models import User
from apps.users.serializers import RegisterSerializer, UserSerializer

@extend_schema(tags=["Auth"])
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = (permissions.AllowAny,)

@extend_schema(tags=["Auth"])
class MeView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        return self.request.user
