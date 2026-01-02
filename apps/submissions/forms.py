from django import forms
from .models import Submission

class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ['description', 'file_upload', 'link']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }
