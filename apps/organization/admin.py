from django.contrib import admin
from .models import ManagerProfile, EmployeeProfile

@admin.register(ManagerProfile)
class ManagerProfileAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'department')
    search_fields = ('user__username', 'user__email', 'user__first_name', 'user__last_name')
    list_select_related = ('user',)

@admin.register(EmployeeProfile)
class EmployeeProfileAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'job_profile', 'department', 'manager', 'status')
    list_filter = ('status', 'department', 'manager')
    search_fields = ('user__username', 'user__email', 'user__first_name', 'user__last_name')
    list_select_related = ('user', 'manager')
    
    # Enables a searchable dropdown for selecting a manager (useful if you have many managers)
    autocomplete_fields = ['manager']
    
    fieldsets = (
        ('Employee Details', {'fields': ('user', 'phone', 'job_profile', 'department', 'profile_picture')}),
        ('Management Assignment', {'fields': ('manager', 'status', 'skills')}),
        ('Contract Info', {'fields': ('contract_start_date', 'contract_months')}),
    )