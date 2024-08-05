from rest_framework.permissions import BasePermission

from .models import Product, Category
from user.models import UserDepartment


class IsStaffInOwnDepartment(BasePermission):
    
    def has_object_permission(self, request, view, obj):
        obj_department = None
        if isinstance(obj, Category):
            obj_department = obj.department
        elif isinstance(obj, Product):
            obj_department = obj.category.department

        return UserDepartment.objects.filter(
            user=request.user,
            department=obj_department,
            is_enabled=True
        ).exists() if obj_department else False


def isUserAndCategoryInTheSameDepartment(user, category):
    try:
        return UserDepartment.objects.filter(
            user=user,
            department=category.department,
            is_enabled=True
        ).exists()
    except:
        return False
