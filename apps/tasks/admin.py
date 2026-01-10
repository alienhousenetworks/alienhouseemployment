from django.contrib import admin
from .models import Task, TimeLog

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'assigned_by', 'due_date', 'priority', 'status', 'is_overdue')
    list_filter = ('status', 'priority', 'due_date')
    search_fields = ('title', 'description')
    filter_horizontal = ('assigned_to',)

@admin.register(TimeLog)
class TimeLogAdmin(admin.ModelAdmin):
    list_display = ('task', 'user', 'hours', 'date')
    list_filter = ('date',)
    search_fields = ('task__title', 'user__full_name')
