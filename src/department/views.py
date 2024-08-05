from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response

from product.models import Category
from product.serializers import CategorySerializer
from .models import Department
from .serializers import DepartmentSerializer


class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save()

    def perform_update(self, serializer):
        instance = serializer.save()
        
    @action(detail=True, methods=['get'])
    def categories(self, request, pk=None):
        department = self.get_object()
        categories = Category.objects.filter(department=department)
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)
