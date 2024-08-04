from typing import Collection
from django.db import models

from base.models import BaseModel
from product.models import Product


class Cart(BaseModel):
    user = models.OneToOneField('user.User', on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f'{self.user} - {self.total_price}'


class CartItem(BaseModel):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    is_enabled = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        unique_together = ('cart', 'product')

    def __str__(self):
        return f'{self.cart} - {self.product}'
    
    def delete(self, using=None, keep_parents=False):
        self.is_deleted = True
        self.is_enabled = False
        self.save()
