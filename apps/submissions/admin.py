from django.contrib import admin
from .models import Submission

@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('task', 'submitted_by', 'status', 'submitted_at', 'reviewed_by')
    list_filter = ('status', 'submitted_at', 'reviewed_at')
    search_fields = ('task__title', 'submitted_by__full_name', 'description')
    readonly_fields = ('submitted_at', 'reviewed_at')
