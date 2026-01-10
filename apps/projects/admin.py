from django.contrib import admin
from .models import Project, Milestone, ProjectTemplate, ResourceAllocation

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'manager', 'status', 'start_date', 'end_date')
    list_filter = ('status', 'start_date', 'end_date')
    search_fields = ('name', 'description')

@admin.register(Milestone)
class MilestoneAdmin(admin.ModelAdmin):
    list_display = ('name', 'project', 'due_date', 'status')
    list_filter = ('status', 'due_date')
    search_fields = ('name', 'project__name')

@admin.register(ResourceAllocation)
class ResourceAllocationAdmin(admin.ModelAdmin):
    list_display = ('user', 'project', 'role', 'allocated_hours')
    list_filter = ('role',)
    search_fields = ('user__full_name', 'project__name')

@admin.register(ProjectTemplate)
class ProjectTemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_by', 'created_at')
    search_fields = ('name', 'description')
