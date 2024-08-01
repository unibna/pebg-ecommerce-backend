from rest_framework import status, viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response

from .models import Category
from .serializers import (
    CategorySerializer,
    CategoryCreateUpdateSerializer,
)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)
    lookup_field = 'pk'
    
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
