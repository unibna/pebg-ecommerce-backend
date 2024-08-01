from django.db import models

from base.models import BaseModel
from department.models import Department


class Category(BaseModel):
    name = models.CharField(max_length=255)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='categories')
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
