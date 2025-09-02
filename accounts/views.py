from rest_framework import viewsets, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import User
from .serializers import UserSerializer, SignupSerializer
from rest_framework_simplejwt.tokens import RefreshToken


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and (request.user.is_superuser or getattr(request.user, 'role', None) == 'admin')


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all().order_by('username')
    serializer_class = UserSerializer
    permission_classes = [IsAdmin]


class SignupView(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = SignupSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        data = {
            "user": UserSerializer(user).data,
            "access": str(refresh.access_token),
            "refresh": str(refresh),
        }
        return Response(data, status=status.HTTP_201_CREATED)
