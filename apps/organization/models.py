from django.db import models
from django.conf import settings
from django.utils.timezone import now
from dateutil.relativedelta import relativedelta

User = settings.AUTH_USER_MODEL

class ManagerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='manager_profile')
    department = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        # Using getattr in case full_name isn't defined on a custom user
        return getattr(self.user, 'full_name', self.user.username)


class EmployeeProfile(models.Model):
    STATUS_CHOICES = (
        ('ACTIVE', 'Active'),
        ('EXPIRED', 'Expired'),
        ('TERMINATED', 'Terminated'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='employee_profile')
    phone = models.CharField(max_length=15)
    job_profile = models.CharField(max_length=255)
    department = models.CharField(max_length=255, blank=True, null=True)
    skills = models.TextField(blank=True, null=True)  # Comma-separated skills
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ACTIVE')

    manager = models.ForeignKey(
        ManagerProfile,
        on_delete=models.SET_NULL,
        null=True,
        blank=True, # Allows the admin/forms to leave it empty
        related_name='employees'
    )

    contract_start_date = models.DateField(default=now)
    contract_months = models.PositiveIntegerField()

    def __str__(self):
        return getattr(self.user, 'full_name', self.user.username)

    # --- Properties must be inside the class ---

    @property
    def contract_end_date(self):
        """Calculates the end date based on contract_start_date and contract_months."""
        if self.contract_start_date:
            return self.contract_start_date + relativedelta(months=self.contract_months)
        return None

    @property
    def is_contract_expired(self):
        """Checks if today's date has passed the contract end date."""
        end_date = self.contract_end_date
        if end_date:
            return now().date() > end_date
        return False

    def save(self, *args, **kwargs):
        if self.is_contract_expired and self.status == 'ACTIVE':
            self.status = 'EXPIRED'
        super().save(*args, **kwargs)
