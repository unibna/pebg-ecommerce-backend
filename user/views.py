from rest_framework import viewsets

from .models import User, UserRole
from .serializers import UserSerializer, UserCreateUpdateSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    
    def get_serializer_class(self):
        if self.action in ['create', 'update']:
            return UserCreateUpdateSerializer
        return UserSerializer
