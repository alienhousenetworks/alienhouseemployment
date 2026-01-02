from django.db import models
from django.conf import settings
from django.utils.timezone import now

User = settings.AUTH_USER_MODEL

class Task(models.Model):
    project = models.ForeignKey('projects.Project', on_delete=models.CASCADE, null=True, blank=True, related_name='tasks')
    PRIORITY_CHOICES = (
        ('LOW', 'Low'),
        ('MEDIUM', 'Medium'),
        ('HIGH', 'High'),
    )

    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('IN_PROGRESS', 'In Progress'),
        ('SUBMITTED', 'Submitted'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
    )

    title = models.CharField(max_length=255)
    description = models.TextField()
    assigned_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assigned_tasks')
    assigned_to = models.ManyToManyField(User, related_name='tasks')
    due_date = models.DateField()
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='MEDIUM')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Task history/comments
    comments = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title

    @property
    def is_overdue(self):
        return now().date() > self.due_date and self.status not in ['APPROVED', 'REJECTED']


class TimeLog(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='time_logs')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='time_logs')
    hours = models.DecimalField(max_digits=5, decimal_places=2)
    date = models.DateField(default=now)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.task.title} - {self.hours} hours"
