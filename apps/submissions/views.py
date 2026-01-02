from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import CreateView, UpdateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.http import HttpResponse, Http404
from django.utils.timezone import now
from .models import Submission
from .forms import SubmissionForm
from apps.tasks.models import Task
from apps.notifications.models import Notification
from apps.core.permissions import is_manager

class SubmissionCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Submission
    form_class = SubmissionForm
    template_name = 'employee/submit_task.html'

    def test_func(self):
        task = get_object_or_404(Task, pk=self.kwargs['task_id'])
        return self.request.user in task.assigned_to.all() and task.status in ['IN_PROGRESS', 'PENDING']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['task'] = get_object_or_404(Task, pk=self.kwargs['task_id'])
        return context

    def form_valid(self, form):
        task = get_object_or_404(Task, pk=self.kwargs['task_id'])
        # Check for duplicate submissions (only one per task per user)
        if Submission.objects.filter(task=task, submitted_by=self.request.user).exists():
            messages.error(self.request, 'You have already submitted for this task.')
            return redirect('tasks:task_list')

        # Check deadline
        if task.due_date < now().date():
            messages.error(self.request, 'Submission deadline has passed.')
            return redirect('tasks:task_list')

        form.instance.task = task
        form.instance.submitted_by = self.request.user
        # Increment version if resubmitting
        last_submission = Submission.objects.filter(task=task, submitted_by=self.request.user).order_by('-version').first()
        form.instance.version = (last_submission.version + 1) if last_submission else 1

        response = super().form_valid(form)

        # Update task status
        task.status = 'SUBMITTED'
        task.save()

        # Create notification for manager
        Notification.objects.create(
            user=task.assigned_by,
            message=f"New submission for task '{task.title}' by {self.request.user.full_name}",
            notification_type='SUBMISSION_CONFIRM',
            task=task
        )

        messages.success(self.request, 'Task submitted successfully.')
        return response

    def get_success_url(self):
        return f"/tasks/{self.kwargs['task_id']}/"

class SubmissionReviewView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Submission
    fields = ['status', 'review_comments']
    template_name = 'manager/review_submission.html'

    def test_func(self):
        submission = self.get_object()
        return is_manager(self.request.user) and submission.task.assigned_by == self.request.user

    def form_valid(self, form):
        submission = form.instance
        submission.reviewed_by = self.request.user
        submission.reviewed_at = now()

        # Update task status based on review
        if submission.status == 'APPROVED':
            submission.task.status = 'APPROVED'
        elif submission.status == 'REJECTED':
            submission.task.status = 'REJECTED'
        elif submission.status == 'REVISION_REQUESTED':
            submission.task.status = 'IN_PROGRESS'
        submission.task.save()

        response = super().form_valid(form)

        # Create notification for employee
        Notification.objects.create(
            user=submission.submitted_by,
            message=f"Your submission for '{submission.task.title}' has been {submission.status.lower()}",
            notification_type='REVIEW',
            task=submission.task
        )

        messages.success(self.request, f'Submission {submission.status.lower()}.')
        return response

    def get_success_url(self):
        return f"/tasks/{self.object.task.pk}/"

class SubmissionDownloadView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Submission

    def test_func(self):
        submission = self.get_object()
        return (is_manager(self.request.user) and submission.task.assigned_by == self.request.user) or \
               (self.request.user == submission.submitted_by)

    def get(self, request, *args, **kwargs):
        submission = self.get_object()
        if submission.file_upload:
            response = HttpResponse(submission.file_upload, content_type='application/octet-stream')
            response['Content-Disposition'] = f'attachment; filename="{submission.file_upload.name}"'
            return response
        raise Http404("File not found")
