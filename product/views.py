from rest_framework import status, viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response

from .models import Category, Product
from .serializers import (
    CategorySerializer,
    CategoryCreateUpdateSerializer,
    ProductSerializer,
    ProductUpdateSerializer,
)
from user.permissions import IsStaff


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)
    lookup_field = 'pk'

    def get_permissions(self):
        if self.action in ['update', 'partial_update']:
            return [IsStaffInDepartment(),] 
        return [IsAuthenticated(),]
    
    def get_queryset(self):
        user = self.request.user
        department = user.departments.first()
        return Category.objects.filter(department=department.id)

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return CategoryCreateUpdateSerializer
        return CategorySerializer

    def perform_create(self, serializer):
        serializer.save()

    def perform_update(self, serializer):
        serializer.save()


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated, IsStaff)
    lookup_field = 'pk'
    
    def get_queryset(self):
        user = self.request.user
        department = user.departments.first()
        return Product.objects.filter(category__department=department.id)

    def get_serializer_class(self):
        if self.action in ['update', 'partial_update']:
            return ProductUpdateSerializer
        return ProductSerializer

    def perform_create(self, serializer):
        user_department = self.request.user.departments.first()
        category = serializer.validated_data['category']
        if category.department.id != user_department.id:
            raise PermissionDenied()
        serializer.save()

    def perform_update(self, serializer):
        obj = self.get_object()
        user_department = self.request.user.departments.first()
        if obj.category.department.id != user_department.id:
            raise PermissionDenied()
        serializer.save()
