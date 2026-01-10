from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.accounts.models import User
from .models import ManagerProfile


@receiver(post_save, sender=User)
def ensure_manager_profile(sender, instance, **kwargs):
    if instance.role == 'MANAGER':
        ManagerProfile.objects.get_or_create(user=instance)


from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import EmployeeProfile

User = settings.AUTH_USER_MODEL


@receiver(post_save, sender=User)
def create_employee_profile(sender, instance, created, **kwargs):
    if created:
        EmployeeProfile.objects.get_or_create(
            user=instance,
            defaults={'contract_months': 12, 'phone': '', 'job_profile': 'Employee'}
        )
