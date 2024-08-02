from rest_framework.permissions import BasePermission

from department.models import Department
from user.enums import UserRoleEnum
from user.models import UserRole, UserDepartment


class IsStaffInOwnDepartment(BasePermission):
    
    def has_permission(self, request, view):
        if not UserRole.objects.filter(
            is_enabled=True,
            role=UserRoleEnum.STAFF.value,
            user=request.user,
        ).exists():
            return False

        if not Department.objects.filter(
            user_department__user=request.user,
        ):
            return False    
        
        if request.user.groups.filter(name='staff').exists():
            user_department = getattr(request.user, 'user_department', None)
            if user_department:
                department = user_department.department
                return True
        return False
