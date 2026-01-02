from rest_framework.permissions import BasePermission
from apps.organization.models import ManagerProfile

class IsAdminOrManager(BasePermission):
    """
    Custom permission to only allow admins or managers to access analytics.
    """
    def has_permission(self, request, view):
        if request.user.is_staff or request.user.is_superuser:
            return True
        # Check if user is a manager
        return ManagerProfile.objects.filter(user=request.user).exists()

class DepartmentAccessPermission(BasePermission):
    """
    Custom permission to allow access to department analytics based on role.
    """
    def has_permission(self, request, view):
        if request.user.is_staff or request.user.is_superuser:
            return True
        # Managers can access their department's analytics
        if ManagerProfile.objects.filter(user=request.user).exists():
            return True
        # Employees can only access their own analytics (handled in views)
        return True

class EmployeeAnalyticsPermission(BasePermission):
    """
    Permission for employees to access only their own analytics.
    """
    def has_object_permission(self, request, view, obj):
        # Employees can only see their own data
        if hasattr(obj, 'user'):
            return obj.user == request.user
        return False
