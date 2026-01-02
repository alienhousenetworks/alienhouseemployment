from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.utils.timezone import now
from .models import Notification
from apps.tasks.models import Task
from apps.organization.models import EmployeeProfile

@shared_task
def send_notification_email(user_email, subject, message):
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [user_email],
        fail_silently=False,
    )

@shared_task
def send_overdue_reminders():
    overdue_tasks = Task.objects.filter(due_date__lt=now().date(), status__in=['PENDING', 'IN_PROGRESS'])
    for task in overdue_tasks:
        for user in task.assigned_to.all():
            Notification.objects.create(
                user=user,
                message=f"Task '{task.title}' is overdue.",
                notification_type='DUE_REMINDER',
                task=task
            )
            send_notification_email.delay(
                user.email,
                'Task Overdue Reminder',
                f"Task '{task.title}' is overdue. Please submit it as soon as possible."
            )

@shared_task
def disable_expired_contracts():
    expired_employees = EmployeeProfile.objects.filter(status='ACTIVE').filter(contract_end_date__lt=now().date())
    expired_employees.update(status='EXPIRED')
