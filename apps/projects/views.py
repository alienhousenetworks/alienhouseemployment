from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.http import JsonResponse
from .models import Project, Milestone, ProjectTemplate, ResourceAllocation
from .forms import ProjectForm, MilestoneForm, ProjectTemplateForm, ResourceAllocationForm
from apps.core.permissions import is_manager

class ProjectListView(LoginRequiredMixin, ListView):
    model = Project
    template_name = 'projects/project_list.html'
    context_object_name = 'projects'
    paginate_by = 10

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'manager_profile'):
            return Project.objects.filter(manager=user)
        elif hasattr(user, 'employee_profile'):
            return Project.objects.filter(resource_allocations__user=user).distinct()
        else:
            return Project.objects.none()

class ProjectDetailView(LoginRequiredMixin, DetailView):
    model = Project
    template_name = 'projects/project_detail.html'
    context_object_name = 'project'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['milestones'] = self.object.milestones.all()
        context['resources'] = self.object.resource_allocations.all()
        return context

class ProjectCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Project
    form_class = ProjectForm
    template_name = 'projects/project_create.html'
    success_url = reverse_lazy('projects:project_list')

    def test_func(self):
        return hasattr(self.request.user, 'manager_profile')

    def form_valid(self, form):
        form.instance.manager = self.request.user
        messages.success(self.request, 'Project created successfully.')
        return super().form_valid(form)

class ProjectUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = 'projects/project_update.html'
    success_url = reverse_lazy('projects:project_list')

    def test_func(self):
        project = self.get_object()
        return project.manager == self.request.user

    def form_valid(self, form):
        messages.success(self.request, 'Project updated successfully.')
        return super().form_valid(form)

class MilestoneCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Milestone
    form_class = MilestoneForm
    template_name = 'projects/milestone_create.html'

    def test_func(self):
        project = get_object_or_404(Project, pk=self.kwargs['project_id'])
        return project.manager == self.request.user

    def form_valid(self, form):
        form.instance.project = get_object_or_404(Project, pk=self.kwargs['project_id'])
        messages.success(self.request, 'Milestone created successfully.')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('projects:project_detail', kwargs={'pk': self.kwargs['project_id']})

class ProjectTemplateListView(LoginRequiredMixin, ListView):
    model = ProjectTemplate
    template_name = 'projects/template_list.html'
    context_object_name = 'templates'
    paginate_by = 10

class ProjectTemplateCreateView(LoginRequiredMixin, CreateView):
    model = ProjectTemplate
    form_class = ProjectTemplateForm
    template_name = 'projects/template_create.html'
    success_url = reverse_lazy('projects:template_list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        messages.success(self.request, 'Template created successfully.')
        return super().form_valid(form)

def instantiate_project_from_template(request, template_id):
    template = get_object_or_404(ProjectTemplate, pk=template_id)
    if request.method == 'POST':
        # Logic to create project from template
        # This is simplified
        project = Project.objects.create(
            name=f"{template.name} Instance",
            description=template.description,
            manager=request.user,
            start_date=request.POST.get('start_date'),
            end_date=request.POST.get('end_date'),
        )
        messages.success(request, 'Project instantiated from template.')
        return redirect('projects:project_detail', pk=project.pk)
    return render(request, 'projects/instantiate_template.html', {'template': template})

class ResourceAllocationCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = ResourceAllocation
    form_class = ResourceAllocationForm
    template_name = 'projects/resource_create.html'

    def test_func(self):
        project = get_object_or_404(Project, pk=self.kwargs['project_id'])
        return project.manager == self.request.user

    def form_valid(self, form):
        form.instance.project = get_object_or_404(Project, pk=self.kwargs['project_id'])
        messages.success(self.request, 'Resource allocated successfully.')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('projects:project_detail', kwargs={'pk': self.kwargs['project_id']})
