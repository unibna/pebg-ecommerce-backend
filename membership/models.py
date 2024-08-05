from enumfields import EnumField
from django.db import models
from django.contrib.auth import get_user_model

from . import enums
from base.models import BaseModel
from cart.models import CartItem
from product.models import Product

User = get_user_model()


class Membership(BaseModel):
    name = models.CharField(max_length=100)
    type = EnumField(enums.MembershipEnum, max_length=10)
    is_enabled = models.BooleanField(default=True)
    rules = models.JSONField(default=dict)
    benefits = models.JSONField(default=dict)
    next_membership = models.ForeignKey(
        'self', 
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='previous_memberships'
    )
