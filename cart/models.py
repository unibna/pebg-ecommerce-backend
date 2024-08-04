from django.db import models

from base.models import BaseModel


class Cart(BaseModel):
    user = models.ForeignKey('user.User', on_delete=models.CASCADE)
    products = models.ManyToManyField('product.Product', through='CartProduct')
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f'{self.user} - {self.total}'
