from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import CreateView, ListView, UpdateView, DetailView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.db.models import Q, Count, Avg, Sum
from django.urls import reverse_lazy
from django.utils.timezone import now
from .models import Task, TimeLog
from .forms import TaskForm, TimeLogForm
from apps.organization.models import EmployeeProfile, ManagerProfile
# from apps.core.permissions import IsManager, IsEmployee

from apps.core.permissions import is_manager, is_employee
from django.http import HttpResponseForbidden


class EmployeeTaskDashboardView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    """
    Enhanced employee dashboard showing all assigned tasks with statistics and filters.
    """
    model = Task
    template_name = 'employee/dashboard_new.html'
    context_object_name = 'tasks'
    paginate_by = 10

    def test_func(self):
        return hasattr(self.request.user, 'employee_profile')

    def get_queryset(self):
        user = self.request.user
        queryset = Task.objects.filter(assigned_to=user)

        # Filter by status
        status = self.request.GET.get('status')
        if status:
            queryset = queryset.filter(status=status)

        # Filter by priority
        priority = self.request.GET.get('priority')
        if priority:
            queryset = queryset.filter(priority=priority)

        return queryset.order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        # Get statistics
        tasks = Task.objects.filter(assigned_to=user)
        context['stats'] = {
            'total': tasks.count(),
            'pending': tasks.filter(status='PENDING').count(),
            'in_progress': tasks.filter(status='IN_PROGRESS').count(),
            'submitted': tasks.filter(status='SUBMITTED').count(),
            'approved': tasks.filter(status='APPROVED').count(),
            'rejected': tasks.filter(status='REJECTED').count(),
            'completed': tasks.filter(status='APPROVED').count(),
            'overdue': tasks.filter(due_date__lt=now().date(), status__in=['PENDING', 'IN_PROGRESS']).count(),
        }
        context['today'] = now()
        return context


class ManagerTaskDashboardView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    """
    Manager dashboard showing all tasks assigned to their team members.
    """
    model = Task
    template_name = 'manager/dashboard_tasks.html'
    context_object_name = 'tasks'
    paginate_by = 15

    def test_func(self):
        return hasattr(self.request.user, 'manager_profile')

    def get_queryset(self):
        user = self.request.user
        queryset = Task.objects.filter(assigned_by=user).prefetch_related('assigned_to', 'submissions')

        # Filter by status
        current_filter = self.request.GET.get('filter', 'all')
        if current_filter == 'pending':
            queryset = queryset.filter(status='PENDING')
        elif current_filter == 'submitted':
            queryset = queryset.filter(status='SUBMITTED')
        elif current_filter == 'completed':
            queryset = queryset.filter(status__in=['APPROVED', 'REJECTED'])
        elif current_filter == 'overdue':
            queryset = queryset.filter(due_date__lt=now().date(), status__in=['PENDING', 'IN_PROGRESS'])

        # Filter by employee
        selected_employee = self.request.GET.get('employee')
        if selected_employee:
            queryset = queryset.filter(assigned_to__id=selected_employee)

        return queryset.distinct().order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        # Get statistics
        tasks = Task.objects.filter(assigned_by=user)
        context['stats'] = {
            'total': tasks.count(),
            'pending': tasks.filter(status='PENDING').count(),
            'in_progress': tasks.filter(status='IN_PROGRESS').count(),
            'submitted': tasks.filter(status='SUBMITTED').count(),
            'approved': tasks.filter(status='APPROVED').count(),
            'rejected': tasks.filter(status='REJECTED').count(),
            'completed': tasks.filter(status='APPROVED').count(),
            'overdue': tasks.filter(due_date__lt=now().date(), status__in=['PENDING', 'IN_PROGRESS']).count(),
        }
        context['today'] = now()
        
        # Get employees for filter
        employees = EmployeeProfile.objects.filter(manager=user.manager_profile)
        context['employees'] = employees
        
        # Add filter context
        context['current_filter'] = self.request.GET.get('filter', 'all')
        context['selected_employee'] = self.request.GET.get('employee')
        
        return context


class TaskCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'manager/task_create.html'
    success_url = reverse_lazy('tasks:task_list')

    def test_func(self):
        return hasattr(self.request.user, 'manager_profile')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def form_valid(self, form):
        form.instance.assigned_by = self.request.user

        # Save the instance first so we can set M2M relationships
        response = super().form_valid(form)

        # If manager explicitly selected assignees, use them; otherwise fallback to manager's team
        selected_users = form.cleaned_data.get('assigned_to')
        if selected_users:
            form.instance.assigned_to.set(selected_users)
        else:
            manager = self.request.user.manager_profile
            employees = EmployeeProfile.objects.filter(manager=manager)
            if form.cleaned_data.get('required_skills'):
                skills = form.cleaned_data['required_skills'].split(',')
                employees = employees.filter(skills__icontains=skills[0])
            user_pks = [e.user.pk for e in employees]
            form.instance.assigned_to.set(user_pks)

        # Create notifications for assigned employees
        from apps.notifications.tasks import send_task_assignment_notifications
        send_task_assignment_notifications.delay(form.instance.id)

        messages.success(self.request, 'Task created successfully.')
        return response

class TaskAcceptView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Task
    fields = []
    template_name = 'employee/task_accept.html'

    def test_func(self):
        task = self.get_object()
        return self.request.user in task.assigned_to.all() and task.status == 'PENDING'

    def form_valid(self, form):
        task = form.instance
        task.status = 'IN_PROGRESS'
        task.save()
        messages.success(self.request, 'Task accepted.')
        return redirect('tasks:task_list')

class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'tasks'
    paginate_by = 10

    def get_template_names(self):
        if hasattr(self.request.user, 'manager_profile'):
            return ['manager/task_list.html']
        else:
            return ['employee/task_list.html']

    def get_queryset(self):
        user = self.request.user
        queryset = Task.objects.all()
        if hasattr(user, 'manager_profile'):
            queryset = queryset.filter(assigned_by=user)
        else:
            queryset = queryset.filter(assigned_to=user)

        status = self.request.GET.get('status')
        if status:
            queryset = queryset.filter(status=status)

        due_date = self.request.GET.get('due_date')
        if due_date:
            queryset = queryset.filter(due_date=due_date)

        return queryset.order_by('-created_at')

class TaskUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Task
    fields = ['status', 'comments']
    template_name = 'task_update.html'
    success_url = reverse_lazy('tasks:task_list')

    def test_func(self):
        task = self.get_object()
        user = self.request.user
        if hasattr(user, 'manager_profile'):
            return task.assigned_by == user
        else:
            return user in task.assigned_to.all()

    def form_valid(self, form):
        messages.success(self.request, 'Task updated successfully.')
        return super().form_valid(form)

class TimeLogCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = TimeLog
    form_class = TimeLogForm
    template_name = 'employee/time_log.html'
    success_url = reverse_lazy('tasks:task_list')

    def test_func(self):
        task_id = self.kwargs['pk']
        task = get_object_or_404(Task, pk=task_id)
        return self.request.user in task.assigned_to.all()

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.task = get_object_or_404(Task, pk=self.kwargs['pk'])
        messages.success(self.request, 'Time logged successfully.')
        return super().form_valid(form)

class TaskReportsView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'manager/task_reports.html'

    def test_func(self):
        return hasattr(self.request.user, 'manager_profile')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        # Task statistics
        tasks = Task.objects.filter(assigned_by=user)
        context['total_tasks'] = tasks.count()
        context['completed_tasks'] = tasks.filter(status='APPROVED').count()
        context['pending_tasks'] = tasks.filter(status='PENDING').count()
        context['in_progress_tasks'] = tasks.filter(status='IN_PROGRESS').count()
        context['rejected_tasks'] = tasks.filter(status='REJECTED').count()
        context['overdue_tasks'] = tasks.filter(due_date__lt=now().date(), status__in=['PENDING', 'IN_PROGRESS']).count()

        # Employee performance
        employees = EmployeeProfile.objects.filter(manager=user.manager_profile)
        employee_stats = []
        for emp in employees:
            emp_tasks = Task.objects.filter(assigned_to=emp.user, assigned_by=user)
            total_time = TimeLog.objects.filter(task__in=emp_tasks).aggregate(total=Sum('hours'))['total'] or 0
            employee_stats.append({
                'employee': emp,
                'total_tasks': emp_tasks.count(),
                'completed_tasks': emp_tasks.filter(status='APPROVED').count(),
                'total_hours': total_time,
            })
        context['employee_stats'] = employee_stats

        # Average completion time
        context['avg_completion_time'] = TimeLog.objects.filter(task__assigned_by=user).aggregate(avg=Avg('hours'))['avg'] or 0

        return context
