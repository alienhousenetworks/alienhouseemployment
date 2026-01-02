from django import forms
from .models import Task, TimeLog

class TaskForm(forms.ModelForm):
    required_skills = forms.CharField(
        max_length=255,
        required=False,
        help_text="Comma-separated skills required for this task (optional)"
    )

    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date', 'priority', 'required_skills']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'due_date': forms.DateInput(attrs={'type': 'date'}),
        }

class TimeLogForm(forms.ModelForm):
    class Meta:
        model = TimeLog
        fields = ['hours', 'date', 'description']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }
