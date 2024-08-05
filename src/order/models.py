from enumfields import EnumField
from django.db import models
from django.contrib.auth import get_user_model

from . import enums
from base.models import BaseModel
from cart.models import CartItem
from product.models import Product
from promotion.handlers.promotion_engine import PromotionEngine

User = get_user_model()


class Order(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    status = EnumField(enums.OrderStatusEnum, max_length=24, 
                    default=enums.OrderStatusEnum.DRAFT)
    origin_total_amount = models.FloatField(default=0.0)
    discount = models.FloatField(default=0.0)
    final_total_amount = models.FloatField(default=0.0)

    def __str__(self):
        return f"Order {self.id} for {self.user.username}"

    def update_origin_total_amount(self):
        self.origin_total_amount = sum(item.total_price for item in self.order_items.all())
        self.save()

    def apply_promotions(self):
        engine = PromotionEngine(self)
        self.discount = engine.apply_promotion()
        final_total_amount = self.origin_total_amount - self.discount
        self.final_total_amount = final_total_amount if final_total_amount > 0 else 0
        self.save()


class OrderItem(BaseModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    price = models.FloatField(default=0.0)

    def __str__(self):
        return f"{self.quantity} x {self.cart_item.product.name} in Order {self.order.id}"

    @property
    def total_price(self):
        return self.quantity * self.price


class OrderPromotion(BaseModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_promotions')
    promotion = models.ForeignKey('promotion.Promotion', on_delete=models.CASCADE)
    is_applied = models.BooleanField(default=False)
