from django import forms
from .models import Project, Milestone, ProjectTemplate, ResourceAllocation

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description', 'start_date', 'end_date', 'status', 'manager']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }

class MilestoneForm(forms.ModelForm):
    class Meta:
        model = Milestone
        fields = ['name', 'description', 'due_date', 'status']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),
        }

class ProjectTemplateForm(forms.ModelForm):
    class Meta:
        model = ProjectTemplate
        fields = ['name', 'description', 'template_data']

class ResourceAllocationForm(forms.ModelForm):
    class Meta:
        model = ResourceAllocation
        fields = ['user', 'role', 'allocated_hours']
