from django.db import models
from django.conf import settings
from django.utils.timezone import now

User = settings.AUTH_USER_MODEL

class KPI(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    value = models.FloatField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='kpis')
    department = models.CharField(max_length=255, blank=True)
    calculated_at = models.DateTimeField(default=now)
    period_start = models.DateField()
    period_end = models.DateField()

    class Meta:
        indexes = [
            models.Index(fields=['user', 'period_start', 'period_end']),
            models.Index(fields=['department', 'period_start', 'period_end']),
        ]

    def __str__(self):
        return f"{self.name} for {self.user.full_name}"

class Report(models.Model):
    REPORT_TYPES = (
        ('PRODUCTIVITY', 'Productivity Report'),
        ('DEPARTMENT', 'Department Analytics'),
        ('TASK_TRENDS', 'Task Trends'),
        ('OVERDUE', 'Overdue Analysis'),
    )

    title = models.CharField(max_length=255)
    report_type = models.CharField(max_length=20, choices=REPORT_TYPES)
    generated_by = models.ForeignKey(User, on_delete=models.CASCADE)
    generated_at = models.DateTimeField(default=now)
    data = models.JSONField()  # Store report data as JSON
    filters = models.JSONField(blank=True, null=True)  # Store applied filters

    class Meta:
        ordering = ['-generated_at']

    def __str__(self):
        return self.title

class AnalyticsCache(models.Model):
    CACHE_TYPES = (
        ('EMPLOYEE_PRODUCTIVITY', 'Employee Productivity'),
        ('DEPARTMENT_METRICS', 'Department Metrics'),
        ('TASK_TRENDS', 'Task Trends'),
    )

    cache_key = models.CharField(max_length=255, unique=True)
    cache_type = models.CharField(max_length=30, choices=CACHE_TYPES)
    data = models.JSONField()
    created_at = models.DateTimeField(default=now)
    expires_at = models.DateTimeField()

    class Meta:
        indexes = [
            models.Index(fields=['cache_type', 'expires_at']),
        ]

    def __str__(self):
        return self.cache_key
