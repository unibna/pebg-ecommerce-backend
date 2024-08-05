from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.core.mail import send_mail

from .models import UserMembership
from cart.models import Cart
from src import settings

User = get_user_model()


@receiver(post_save, sender=User)
def create_cart_for_new_user(sender, instance, created, **kwargs):
    if created:
        Cart.objects.create(user=instance)
        
        
@receiver(post_save, sender=User)
def create_user_membership_for_new_user(sender, instance, created, **kwargs):
    if created:
        UserMembership.objects.create(user=instance)


@receiver(post_save, sender=User)
def send_activation_email(sender, instance, created, **kwargs):
    if created:
        activation_link = f"http://localhost:8000/api/activate/?token={instance.activation_token}"
        subject = 'Activate your account'
        message = f'Hi {instance.email},\n\nPlease click the link below to activate your account:\n{activation_link}\n\nThank you!'
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [instance.email])
