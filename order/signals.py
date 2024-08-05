from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

from .models import Order
from .enums import OrderStatusEnum
from membership.models import Membership
from membership.handlers import can_move_next_membership
from user.models import UserMembership

User = get_user_model()


@receiver(post_save, sender=Order)
def update_user_membership(sender, instance, **kwargs):
    if instance.status == OrderStatusEnum.COMPLETED:
        user = instance.user
        current_membership = user.membership.first()
        total_completed_order = user.orders.filter(
            status=OrderStatusEnum.COMPLETED
        ).count()
        
        if current_membership:
            if can_move_next_membership(
                user=user,
                achievement={'total_completed_order': total_completed_order},
                current_membership=current_membership,
            ):
                user.membership = current_membership.next_membership
                user.save()
        else:
            memberships = Membership.objects.filter(is_enabled=True)
            for membership in memberships:
                if can_move_next_membership(
                    user=user,
                    achievement={'total_completed_order': total_completed_order},
                    current_membership=None,
                    next_membership=membership,
                ):
                    UserMembership.objects.create(
                        user=user,
                        membership=membership
                    )
                    break