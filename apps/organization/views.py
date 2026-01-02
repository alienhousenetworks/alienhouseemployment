from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Count, Q, Avg
from django.utils.timezone import now
from .models import EmployeeProfile, ManagerProfile
from apps.tasks.models import Task, TimeLog
from apps.submissions.models import Submission
from apps.core.permissions import is_manager

class EmployeeDashboardView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'employee/dashboard.html'

    def test_func(self):
        return hasattr(self.request.user, 'employee_profile')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        # Task stats
        assigned_tasks = Task.objects.filter(assigned_to=user)
        context['total_tasks'] = assigned_tasks.count()
        context['pending_tasks'] = assigned_tasks.filter(status='PENDING').count()
        context['in_progress_tasks'] = assigned_tasks.filter(status='IN_PROGRESS').count()
        context['completed_tasks'] = assigned_tasks.filter(status__in=['APPROVED', 'REJECTED']).count()
        context['overdue_tasks'] = assigned_tasks.filter(due_date__lt=now().date(), status__in=['PENDING', 'IN_PROGRESS']).count()

        # Recent tasks
        context['recent_tasks'] = assigned_tasks.order_by('-created_at')[:5]

        # Time logged this month
        this_month = now().replace(day=1)
        context['time_logged_this_month'] = TimeLog.objects.filter(
            user=user, date__gte=this_month
        ).aggregate(total_hours=Avg('hours'))['total_hours'] or 0

        return context

class ManagerDashboardView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'manager/dashboard.html'

    def test_func(self):
        return is_manager(self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        # Task stats
        created_tasks = Task.objects.filter(assigned_by=user)
        context['total_tasks_created'] = created_tasks.count()
        context['pending_reviews'] = Submission.objects.filter(task__assigned_by=user, status='PENDING').count()
        context['approved_tasks'] = created_tasks.filter(status='APPROVED').count()
        context['rejected_tasks'] = created_tasks.filter(status='REJECTED').count()

        # Employee stats
        employees = EmployeeProfile.objects.filter(manager=user.manager_profile)
        context['total_employees'] = employees.count()
        context['active_employees'] = employees.filter(status='ACTIVE').count()

        # Recent activities
        context['recent_tasks'] = created_tasks.order_by('-created_at')[:5]
        context['recent_submissions'] = Submission.objects.filter(task__assigned_by=user).order_by('-submitted_at')[:5]

        # Performance metrics
        context['avg_completion_time'] = TimeLog.objects.filter(task__assigned_by=user).aggregate(avg_hours=Avg('hours'))['avg_hours'] or 0

        return context
