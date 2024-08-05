from django.db import transaction
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError, NotFound, PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView


from . import models, serializers
from user.permissions import IsStaff


class MembershipViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = models.Membership.objects.all()
    serializer_class = serializers.MembershipSerializer
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsStaff()]
        return super().get_permissions()
    
    def get_queryset(self):
        return self.queryset.filter(is_enabled=True)
    
    def get_serializer_class(self):
        if self.action in ['update', 'partial_update']:
            return serializers.MembershipUpdateSerializer
        return self.serializer_class
