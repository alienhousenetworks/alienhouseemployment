from django.db import models
from django.conf import settings
from django.utils.timezone import now

User = settings.AUTH_USER_MODEL

class Project(models.Model):
    STATUS_CHOICES = (
        ('PLANNING', 'Planning'),
        ('IN_PROGRESS', 'In Progress'),
        ('ON_HOLD', 'On Hold'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    )

    name = models.CharField(max_length=255)
    description = models.TextField()
    manager = models.ForeignKey(User, on_delete=models.CASCADE, related_name='managed_projects')
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PLANNING')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    @property
    def is_overdue(self):
        return now().date() > self.end_date and self.status not in ['COMPLETED', 'CANCELLED']

class Milestone(models.Model):
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('IN_PROGRESS', 'In Progress'),
        ('COMPLETED', 'Completed'),
    )

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='milestones')
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    due_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.project.name} - {self.name}"

class ProjectTemplate(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    template_data = models.JSONField()  # Store tasks, milestones, etc. as JSON
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class ResourceAllocation(models.Model):
    ROLE_CHOICES = (
        ('LEAD', 'Project Lead'),
        ('DEVELOPER', 'Developer'),
        ('TESTER', 'Tester'),
        ('DESIGNER', 'Designer'),
        ('ANALYST', 'Business Analyst'),
    )

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='resource_allocations')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='project_allocations')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    allocated_hours = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.full_name} - {self.project.name} ({self.role})"
