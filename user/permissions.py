from rest_framework import permissions

from .enums import UserRoleEnum
from .models import UserDepartment, UserRole
from product.models import Category, Product


class IsSelfOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj == request.user


class IsStaff(permissions.BasePermission):
    
    def has_permission(self, request, view):
        if not UserRole.objects.filter(
            is_enabled=True,
            role=UserRoleEnum.STAFF.value,
            user=request.user,
        ).exists():
            return False
        return True
