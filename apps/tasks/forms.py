from django import forms
from django.contrib.auth import get_user_model
from .models import Task, TimeLog
from apps.organization.models import EmployeeProfile

User = get_user_model()


class TaskForm(forms.ModelForm):
    required_skills = forms.CharField(
        max_length=255,
        required=False,
        help_text="Comma-separated skills required for this task (optional)"
    )

    assigned_to = forms.ModelMultipleChoiceField(
        queryset=User.objects.none(),
        required=False,
        widget=forms.SelectMultiple(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date', 'priority', 'required_skills', 'assigned_to']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'due_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        # If a manager user is provided, populate the assigned_to queryset
        if user and hasattr(user, 'manager_profile'):
            manager = user.manager_profile
            employees = EmployeeProfile.objects.filter(manager=manager).select_related('user')
            user_qs = User.objects.filter(pk__in=[e.user.pk for e in employees])
            self.fields['assigned_to'].queryset = user_qs
        else:
            # Non-managers shouldn't see any options by default
            self.fields['assigned_to'].queryset = User.objects.none()

class TimeLogForm(forms.ModelForm):
    class Meta:
        model = TimeLog
        fields = ['hours', 'date', 'description']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }
