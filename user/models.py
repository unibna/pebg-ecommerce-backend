import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from enumfields import EnumField

from base.models import BaseModel
from .managers import UserManager
from .enums import UserRoleEnum


class User(AbstractUser):
    objects = UserManager()

    username = None
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=False)
    activation_token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    activated_time = models.DateTimeField(null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    def activate(self):
        self.is_active = True
        self.activated_time = timezone.now()
        self.save()


class UserRole(BaseModel):
    is_enabled = models.BooleanField(default=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='roles')
    role = EnumField(UserRoleEnum, max_length=255)

    class Meta:
        unique_together = ('user', 'role')

    def __str__(self):
        return self.role.value
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.role == UserRoleEnum.STAFF and self.is_enabled:
            self.user.is_staff = True
            self.user.save()


class UserDepartment(BaseModel):
    is_enabled = models.BooleanField(default=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='departments')
    department = models.ForeignKey('department.Department', on_delete=models.CASCADE, related_name='users')

    class Meta:
        unique_together = ('user', 'department')

    def __str__(self):
        return self.department.name
    
    def save(self, *args, **kwargs):
        if self.is_enabled:
            UserDepartment.objects.filter(
                user=self.user
            ).update(
                is_enabled=False
            )
        super().save(*args, **kwargs)
