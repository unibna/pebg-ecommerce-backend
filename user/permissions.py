from rest_framework import permissions

from .enums import UserRoleEnum
from .models import User, UserRole
from product.models import Category, Product


class IsSelfOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        obj_user = None
        if isinstance(obj, User):
            obj_user = obj
        elif hasattr(obj, 'user'):
            obj_user = obj.user

        return obj_user.id == request.user.id if obj_user else False


class IsStaff(permissions.BasePermission):
    
    def has_permission(self, request, view):
        print("-----> check permission")
        if UserRole.objects.filter(
            is_enabled=True,
            role=UserRoleEnum.STAFF.value,
            user=request.user,
        ).exists():
            return True
        return False
