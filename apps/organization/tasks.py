# employee_mgmt/apps/organization/tasks.py

from celery import shared_task
from django.contrib.auth import get_user_model
from django.core.mail import send_mail

User = get_user_model()

@shared_task(bind=True, autoretry_for=(Exception,), retry_kwargs={'max_retries': 3, 'countdown': 5})
def send_email_to_user(self, user_id, subject, message):
    try:
        user = User.objects.get(id=user_id)

        send_mail(
            subject=subject,
            message=message,
            from_email=None,  # uses DEFAULT_FROM_EMAIL
            recipient_list=[user.email],
            fail_silently=False,
        )

    except User.DoesNotExist:
        return f"User {user_id} does not exist"


from celery import shared_task

@shared_task(bind=True, autoretry_for=(Exception,), retry_backoff=10, retry_kwargs={'max_retries': 3})
def bulk_create_employees_task(self, file_path, created_by_user_id):
    from django.contrib.auth import get_user_model
    from .services import bulk_create_employees
    User = get_user_model()

    user = User.objects.get(id=created_by_user_id)

    with open(file_path, 'rb') as f:
        bulk_create_employees(f, user)
