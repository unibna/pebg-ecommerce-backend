
from django.db.models import Q
from rest_framework import status, viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response

from .models import User, UserRole
from .serializers import (
    UserActivationSerializer,
    UserSerializer,
    UserCreateSerializer,
    UserUpdateSerializer,
    UserRoleSerializer,
    UserRoleCreateSerializer,
    UserRoleUpdateSerializer
)
from .permissions import IsSelfOrReadOnly


class UserActivateAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserActivationSerializer(data=request.data)
        if serializer.is_valid():
            activation_token = serializer.validated_data['activation_token']
            try:
                user = User.objects.get(activation_token=activation_token, is_active=False)
                user.activate()
                return Response(
                    {'detail': 'Account activated successfully.'},
                    status=status.HTTP_200_OK
                )
            except User.DoesNotExist:
                return Response(
                    {'detail': 'Invalid activation token.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated, IsSelfOrReadOnly)

    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
        elif self.action == 'update':
            return UserUpdateSerializer
        return UserSerializer
    
    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]
        return [IsAuthenticated()]
    
    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)
    
    def get_object(self):
        obj = super().get_object()
        if obj != self.request.user:
            raise PermissionDenied("You do not have permission to access this resource.")
        return obj

    def perform_update(self, serializer):
        serializer.save()
    

class UserRoleViewSet(viewsets.ModelViewSet):
    queryset = UserRole.objects.all()
    serializer_class = UserRoleSerializer
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)
    lookup_field = 'pk'

    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        if user_id:
            return UserRole.objects.filter(user_id=user_id)
        return UserRole.objects.all()

    def get_serializer_class(self):
        if self.action in ['create']:
            return UserRoleCreateSerializer
        if self.action in ['update', 'partial_update']:
            return UserRoleUpdateSerializer
        return UserRoleSerializer

    def perform_create(self, serializer):
        serializer.save()

    def perform_update(self, serializer):
        serializer.save()
