from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL

class Submission(models.Model):
    STATUS_CHOICES = (
        ('PENDING', 'Pending Review'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
        ('REVISION_REQUESTED', 'Revision Requested'),
    )

    task = models.ForeignKey('tasks.Task', on_delete=models.CASCADE, related_name='submissions')
    submitted_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='submissions')
    submitted_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Submission content
    description = models.TextField(blank=True, null=True)
    file_upload = models.FileField(upload_to='submissions/', blank=True, null=True)
    link = models.URLField(blank=True, null=True)

    # Review details
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    reviewed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='reviewed_submissions')
    reviewed_at = models.DateTimeField(null=True, blank=True)
    review_comments = models.TextField(blank=True, null=True)

    # Versioning (for multiple submissions per task)
    version = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"Submission for {self.task.title} by {self.submitted_by.full_name}"

    class Meta:
        ordering = ['-submitted_at']
        unique_together = ['task', 'submitted_by', 'version']
