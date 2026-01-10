from django.shortcuts import redirect
from django.views.generic import TemplateView, ListView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import models
from django.db.models import Avg
from django.utils.timezone import now
from .models import EmployeeProfile
from apps.tasks.models import Task, TimeLog
from apps.submissions.models import Submission
from apps.core.mixins import ManagerRequiredMixin, EmployeeRequiredMixin

class EmployeeDashboardView(
    LoginRequiredMixin,
    EmployeeRequiredMixin,
    TemplateView
):
    template_name = 'employee/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        assigned_tasks = Task.objects.filter(assigned_to=user)

        context.update({
            'total_tasks': assigned_tasks.count(),
            'pending_tasks': assigned_tasks.filter(status='PENDING').count(),
            'in_progress_tasks': assigned_tasks.filter(status='IN_PROGRESS').count(),
            'completed_tasks': assigned_tasks.filter(
                status__in=['APPROVED', 'REJECTED']
            ).count(),
            'overdue_tasks': assigned_tasks.filter(
                due_date__lt=now().date(),
                status__in=['PENDING', 'IN_PROGRESS']
            ).count(),
            'recent_tasks': assigned_tasks.order_by('-created_at')[:5],
        })

        this_month = now().replace(day=1)
        context['time_logged_this_month'] = (
            TimeLog.objects.filter(user=user, date__gte=this_month)
            .aggregate(avg_hours=Avg('hours'))['avg_hours'] or 0
        )

        return context

    def post(self, request, *args, **kwargs):
        return redirect(request.path)


class ManagerDashboardView(
    LoginRequiredMixin,
    ManagerRequiredMixin,
    TemplateView
):
    template_name = 'manager/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        manager = user.manager_profile

        created_tasks = Task.objects.filter(assigned_by=user)
        employees = EmployeeProfile.objects.filter(manager=manager)

        pending_reviews_qs = Submission.objects.filter(
            task__assigned_by=user,
            status='PENDING'
        )

        context.update({
            'total_tasks_created': created_tasks.count(),
            'pending_reviews': pending_reviews_qs,
            'pending_reviews_count': pending_reviews_qs.count(),
            'approved_tasks': created_tasks.filter(status='APPROVED').count(),
            'rejected_tasks': created_tasks.filter(status='REJECTED').count(),
            'total_employees': employees.count(),
            'active_employees': employees.filter(status='ACTIVE').count(),
            'recent_tasks': created_tasks.order_by('-created_at')[:5],
            'recent_submissions': Submission.objects.filter(
                task__assigned_by=user
            ).order_by('-submitted_at')[:5],
            'avg_completion_time': (
                TimeLog.objects.filter(task__assigned_by=user)
                .aggregate(avg_hours=Avg('hours'))['avg_hours'] or 0
            ),
        })

        return context



class EmployeeListView(LoginRequiredMixin, ListView):
    model = EmployeeProfile
    template_name = 'organization/employee_list.html'
    context_object_name = 'employees'

    def get_queryset(self):
        user = self.request.user
        query = self.request.GET.get('q', '')

        if user.role == 'MANAGER':
            if hasattr(user, 'manager_profile'):
                queryset = EmployeeProfile.objects.filter(
                    manager=user.manager_profile
                )
            else:
                return EmployeeProfile.objects.none()
        elif user.is_staff or user.is_superuser:
            queryset = EmployeeProfile.objects.all()
        else:
            return EmployeeProfile.objects.none()

        # Search by employee_id, name, or email
        if query:
            queryset = queryset.filter(
                models.Q(employee_id__icontains=query) |
                models.Q(user__full_name__icontains=query) |
                models.Q(user__email__icontains=query)
            )

        return queryset


class AssignManagerView(LoginRequiredMixin, UpdateView):
    model = EmployeeProfile
    fields = ['manager']
    template_name = 'organization/assign_manager.html'
    success_url = reverse_lazy('organization:employee_list')

    def dispatch(self, request, *args, **kwargs):
        # Ensure only Admins (Staff/Superuser) can access this view
        if not (request.user.is_staff or request.user.is_superuser):
            from django.core.exceptions import PermissionDenied
            raise PermissionDenied("You do not have permission to assign managers.")
        
        return super().dispatch(request, *args, **kwargs)
