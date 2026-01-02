from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL

class Notification(models.Model):
    NOTIFICATION_TYPES = (
        ('ASSIGNMENT', 'Task Assignment'),
        ('DUE_REMINDER', 'Due Date Reminder'),
        ('SUBMISSION_CONFIRM', 'Submission Confirmation'),
        ('REVIEW', 'Submission Review'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES, default='ASSIGNMENT')
    task = models.ForeignKey('tasks.Task', on_delete=models.CASCADE, null=True, blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user.username}: {self.notification_type}"
