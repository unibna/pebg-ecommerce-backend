from rest_framework import status, viewsets
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response

from .models import Category, Product
from .serializers import (
    CategorySerializer,
    CategoryCreateSerializer,
    CategoryUpdateSerializer,
    ProductSerializer,
    ProductUpdateSerializer,
)
from .permissions import (
    IsStaffInOwnDepartment,
    isUserAndCategoryInTheSameDepartment,
)
from user.models import UserDepartment
from user.permissions import IsStaff


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    authentication_classes = (JWTAuthentication,)
    lookup_field = 'pk'

    def get_permissions(self):
        if self.action in ['update', 'partial_update']:
            return [IsStaffInOwnDepartment(),] 
        return [IsAuthenticated(), IsStaff(),]

    def get_queryset(self):
        user_department = UserDepartment.objects.filter(
            user=self.request.user,
            is_enabled=True
        ).first()
        categories = Category.objects.filter(
            department=user_department.department.id
        ) if user_department else Category.objects.none()
        return categories

    def get_serializer_class(self):
        if self.action == 'create':
            return CategoryCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return CategoryUpdateSerializer
        return CategorySerializer

    def perform_create(self, serializer):
        if Category.objects.filter(
            name=serializer.validated_data['name'],
            department=serializer.validated_data['department']
        ).exists():
            raise ValidationError({"detail": "Category already exists"})
        serializer.save()

    def perform_update(self, serializer):
        serializer.save()


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated, IsStaffInOwnDepartment)
    lookup_field = 'pk'
    
    def get_queryset(self):
        if self.request.user.is_staff:
            user_department = UserDepartment.objects.filter(
                user=self.request.user,
                is_enabled=True
            ).first()
            return Product.objects.filter(
                category__department=user_department.department.id
            ) if user_department else Product.objects.none()
        else:
            return Product.objects.filter(is_enabled=True)
        
    def get_permissions(self):
        if self.request.user.is_staff:
            return (IsAuthenticated(), IsStaffInOwnDepartment())
        else:
            if self.action in ['create', 'update', 'partial_update']:
                raise PermissionDenied()
            return (IsAuthenticated(),)

    def get_serializer_class(self):
        if self.action in ['update', 'partial_update']:
            return ProductUpdateSerializer
        return ProductSerializer

    def perform_create(self, serializer):
        if not UserDepartment.objects.filter(
            user=self.request.user,
            department=serializer.validated_data['category'].department,
            is_enabled=True
        ).exists():
            raise PermissionDenied()
        serializer.save()

    def perform_update(self, serializer):
        serializer.save()
