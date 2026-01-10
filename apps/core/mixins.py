from django.core.exceptions import PermissionDenied


class ManagerRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        user = request.user

        if not user.is_authenticated:
            raise PermissionDenied("Login required")

        if user.role != 'MANAGER':
            raise PermissionDenied("Managers only")

        if not hasattr(user, 'manager_profile'):
            # Auto-create profile if missing to prevent 403 error
            from apps.organization.models import ManagerProfile
            ManagerProfile.objects.create(user=user)

        return super().dispatch(request, *args, **kwargs)


class EmployeeRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        user = request.user

        if not user.is_authenticated:
            raise PermissionDenied("Login required")

        if user.role != 'EMPLOYEE':
            raise PermissionDenied("Employees only")

        if not hasattr(user, 'employee_profile'):
            # Auto-create profile if missing to prevent 403 error
            from apps.organization.models import EmployeeProfile
            EmployeeProfile.objects.get_or_create(
                user=user,
                defaults={'contract_months': 12, 'phone': '', 'job_profile': 'Employee'}
            )


        return super().dispatch(request, *args, **kwargs)
