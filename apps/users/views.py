from rest_framework import generics, permissions, status
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from apps.users.models import User
from apps.users.serializers import RegisterSerializer, UserSerializer


class UnwrapUserMixin:
    def get_serializer(self, *args, **kwargs):
        if "data" in kwargs:
            kwargs["data"] = kwargs["data"].get("user", kwargs["data"])
        return super().get_serializer(*args, **kwargs)

@extend_schema(tags=["Auth"])
class SignOutView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        return Response(status=status.HTTP_204_NO_CONTENT)

@extend_schema(tags=["Auth"])
class RegisterView(UnwrapUserMixin, generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = (permissions.AllowAny,)
    authentication_classes = []
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        response = Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
        response["Authorization"] = f"Bearer {str(refresh.access_token)}"
        return response
    
@extend_schema(tags=["Auth"])
class SignInView(UnwrapUserMixin, TokenObtainPairView):
    authentication_classes = []
    
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        access_token = response.data.get("access")
        data = request.data.get("user", request.data)
        user = User.objects.get(email=data.get("email"))
        new_response = Response(UserSerializer(user).data, status=status.HTTP_200_OK)
        new_response["Authorization"] = f"Bearer {access_token}"
        return new_response

@extend_schema(tags=["Auth"])
class MeView(UnwrapUserMixin, generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        return self.request.user
