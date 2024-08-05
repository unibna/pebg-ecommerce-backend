from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

from .models import UserMembership
from cart.models import Cart

User = get_user_model()


@receiver(post_save, sender=User)
def create_cart_for_new_user(sender, instance, created, **kwargs):
    if created:
        Cart.objects.create(user=instance)
        
        
@receiver(post_save, sender=User)
def create_user_membership_for_new_user(sender, instance, created, **kwargs):
    if created:
        UserMembership.objects.create(user=instance)
