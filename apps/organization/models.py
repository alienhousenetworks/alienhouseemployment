from django.db import models
from django.conf import settings
from django.utils.timezone import now
from dateutil.relativedelta import relativedelta
from django.utils import timezone

User = settings.AUTH_USER_MODEL

class ManagerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='manager_profile')
    department = models.CharField(max_length=255, blank=True, null=True)

    # def __str__(self):
    #     # Using getattr in case full_name isn't defined on a custom user
    #     return getattr(self.user, 'full_name', self.user.username)
    def __str__(self):
        return self.user.full_name or self.user.email



class EmployeeProfile(models.Model):
    STATUS_CHOICES = (
        ('ACTIVE', 'Active'),
        ('EXPIRED', 'Expired'),
        ('TERMINATED', 'Terminated'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='employee_profile')
    employee_id = models.CharField(max_length=50, unique=True, blank=True, null=True, editable=False)
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

    # def __str__(self):
    #     return getattr(self.user, 'full_name', self.user.username)
    def __str__(self):
        return self.user.full_name or self.user.email

    # --- Properties must be inside the class ---

    # @property
    # def contract_end_date(self):
    #     """Calculates the end date based on contract_start_date and contract_months."""
    #     if self.contract_start_date:
    #         return self.contract_start_date + relativedelta(months=self.contract_months)
    #     return None
    @property
    def contract_end_date(self):
        if not self.contract_start_date or not self.contract_months:
            return None
        return self.contract_start_date + relativedelta(months=int(self.contract_months))


    # @property
    # def is_contract_expired(self):
    #     """Checks if today's date has passed the contract end date."""
    #     end_date = self.contract_end_date
    #     if end_date:
    #         return now().date() > end_date
    #     return False

    # @property
    # def is_contract_expired(self):
    #     end_date = self.contract_end_date
    #     if not end_date:
    #         return False
    #     return end_date < timezone.now().date()
    @property
    def is_contract_expired(self):
        if self.contract_end_date is None:
            return False  # Contract end not set yet
        return self.contract_end_date < timezone.now().date()

    def generate_employee_id(self):
        """Generate unique employee ID in format: ahn_role_MMYYYY_######"""
        from django.db import transaction
        
        if self.employee_id:
            return self.employee_id
            
        # Get role prefix (uppercase)
        role = self.user.role.upper() if self.user.role else 'EMPLOYEE'
        
        # Get joining month and year from contract_start_date
        if self.contract_start_date:
            month = self.contract_start_date.month
            year = self.contract_start_date.year
        else:
            # Default to current date if not set
            from django.utils.timezone import now
            current = now().date()
            month = current.month
            year = current.year
        
        # Format: MMYYYY
        joining_info = f"{month:02d}{year}"
        
        with transaction.atomic():
            # Get the last employee_id with same role and joining month/year
            prefix = f"ahn_{role.lower()}_{joining_info}_"
            existing_ids = EmployeeProfile.objects.filter(
                employee_id__startswith=prefix
            ).values_list('employee_id', flat=True)
            
            # Extract sequence numbers and find the max
            max_seq = 0
            for emp_id in existing_ids:
                if emp_id and emp_id.startswith(prefix):
                    try:
                        seq_str = emp_id.replace(prefix, '')
                        seq = int(seq_str)
                        if seq > max_seq:
                            max_seq = seq
                    except (ValueError, AttributeError):
                        continue
            
            # Generate new sequence (6 digits, expandable)
            new_seq = max_seq + 1
            self.employee_id = f"{prefix}{new_seq:06d}"
        
        return self.employee_id

    def save(self, *args, **kwargs):
        # Generate employee_id if not set
        if not self.employee_id:
            self.generate_employee_id()
        
        # Update status based on contract expiration
        if self.is_contract_expired and self.status == 'ACTIVE':
            self.status = 'EXPIRED'
        
        super().save(*args, **kwargs)
