from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User
from apps.organization.tasks import send_email_to_user

@receiver(post_save, sender=User)
def send_welcome_email(sender, instance, created, **kwargs):
    if created and instance.role == 'EMPLOYEE':
        send_email_to_user.delay(
            instance.id,
            "Welcome to AlienHouse",
            "Your account has been created successfully."
        )
