from django.db import models

from base.models import BaseModel
from department.models import Department


class Category(BaseModel):
    name = models.CharField(max_length=255)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='categories')
    description = models.TextField(blank=True, null=True)
    is_enabled = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Product(BaseModel):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    description = models.TextField(blank=True, null=True)
    price = models.FloatField(default=0.0)
    stock = models.IntegerField(default=0)
    is_enabled = models.BooleanField(default=True)

    def __str__(self):
        return self.name
