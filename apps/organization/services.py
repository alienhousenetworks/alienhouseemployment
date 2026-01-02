import csv
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail

from apps.accounts.models import User
from .models import EmployeeProfile, ManagerProfile


# def send_employee_invite_email(user):
#     token = default_token_generator.make_token(user)
#     link = f"{settings.FRONTEND_URL}/set-password/{user.id}/{token}/"

#     send_mail(
#         subject="AlienHouse Employee Access",
#         message=f"""
# Hello {user.full_name},

# Your employee account has been created.

# Set your password using the link below:
# {link}

# Regards,
# AlienHouse HR
# """,
#         from_email=settings.DEFAULT_FROM_EMAIL,
#         recipient_list=[user.email],
#     )




from apps.organization.tasks import send_email_to_user

def send_employee_invite_email(user):
    send_email_to_user.delay(
        user.id,
        "AlienHouse Employee Access",
        f"""
Hello {user.full_name},

Your employee account has been created.

Set your password using the link below:
{settings.FRONTEND_URL}/set-password/{user.id}/{token}/
"""
    )


def bulk_create_employees(file, created_by_user):
    reader = csv.DictReader(file.read().decode().splitlines())

    for row in reader:
        user, created = User.objects.get_or_create(
            email=row['Email'].lower(),
            defaults={
                'full_name': row['Name'],
                'phone': row['Phone'],
                'role': 'EMPLOYEE',
            }
        )

        if created:
            user.set_unusable_password()
            user.save()
            send_employee_invite_email(user)

        if created_by_user.role == 'MANAGER':
            manager = ManagerProfile.objects.get(user=created_by_user)
        else:
            manager_user = User.objects.get(
                email=row['Manager Email'],
                role='MANAGER'
            )
            manager = ManagerProfile.objects.get(user=manager_user)

        EmployeeProfile.objects.get_or_create(
            user=user,
            defaults={
                'phone': row['Phone'],
                'job_profile': row['Job Profile'],
                'manager': manager,
                'contract_months': int(row['Contract Months']),
            }
        )


def export_employee_master_sheet():
    employees = EmployeeProfile.objects.select_related(
        'user',
        'manager__user'
    )

    rows = []
    for e in employees:
        rows.append({
            'Name': e.user.full_name,
            'Email': e.user.email,
            'Phone': e.phone,
            'Job Profile': e.job_profile,
            'Manager': e.manager.user.full_name if e.manager else '',
            'Created At': e.created_at.strftime('%Y-%m-%d'),
            'Contract Months': e.contract_months,
        })

    return rows
