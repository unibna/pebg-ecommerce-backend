from rest_framework import status, viewsets
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response

from .models import User, UserRole, UserDepartment, UserMembership
from .serializers import (
    MeSerializer,
    UserActivationSerializer,
    UserSerializer,
    UserCreateSerializer,
    UserUpdateSerializer,
    UserRoleSerializer,
    UserRoleCreateSerializer,
    UserRoleUpdateSerializer,
    UserDepartmentSerializer,
    UserDepartmentCreateSerializer,
    UserDepartmentUpdateSerializer,
    UserMembershipSerializer,
)
from .permissions import IsSelfOrReadOnly, IsStaff


class MeAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = MeSerializer(request.user)
        return Response(serializer.data)


class UserActivateAPIView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        activation_token = request.query_params.get('token')
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
        
        return Response({'detail': 'Account activated successfully.'}, status=status.HTTP_200_OK)

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
    authentication_classes = [JWTAuthentication]

    def get_serializer_class(self):
        if self.action == 'create':
            raise PermissionDenied("Method not allowed.")
        elif self.action == 'update':
            return UserUpdateSerializer
        return UserSerializer
    
    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]
        return [IsSelfOrReadOnly()]

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)
    
    def get_object(self):
        obj = super().get_object()
        if obj != self.request.user:
            raise PermissionDenied("You do not have permission to access this resource.")
        return obj
    
    def perform_update(self, serializer):
        serializer.save()
        
        
class RegisterAPIView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserRoleViewSet(viewsets.ModelViewSet):
    queryset = UserRole.objects.all()
    serializer_class = UserRoleSerializer
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated, IsSelfOrReadOnly)
    lookup_field = 'pk'
    
    def get_queryset(self):
        return UserRole.objects.filter(user_id=self.request.user.id)

    def get_serializer_class(self):
        if self.action in ['create']:
            return UserRoleCreateSerializer
        if self.action in ['update', 'partial_update']:
            return UserRoleUpdateSerializer
        return UserRoleSerializer
    
    def perform_create(self, serializer):
        user = self.request.user
        role = serializer.validated_data.get('role')

        if UserRole.objects.filter(user=user, role=role).exists():
            raise ValidationError({"detail": "User already assigned to this role."})
        
        serializer.save()

    def perform_update(self, serializer):
        serializer.save()


class UserDepartmentViewSet(viewsets.ModelViewSet):
    queryset = UserDepartment.objects.all()
    serializer_class = UserDepartmentSerializer
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)
    lookup_field = 'pk'

    def get_queryset(self):
        return UserDepartment.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action in ['create']:
            return UserDepartmentCreateSerializer
        if self.action in ['update', 'partial_update']:
            return UserDepartmentUpdateSerializer
        return UserDepartmentSerializer

    def perform_create(self, serializer):
        user = self.request.user
        department = serializer.validated_data.get('department')

        if UserDepartment.objects.filter(user=user, department=department).exists():
            raise ValidationError({"detail": "User already assigned to this department."})
        
        serializer.save()

    def perform_update(self, serializer):
        serializer.save()


class UserMembershipViewSet(viewsets.ModelViewSet):
    queryset = UserMembership.objects.all()
    serializer_class = UserMembershipSerializer
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)
    lookup_field = 'pk'
    
    def get_queryset(self):
        return UserMembership.objects.filter(user=self.request.user)
    
    def get_permission(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            raise PermissionDenied("Method not allowed.")
        return super().get_permissions()
