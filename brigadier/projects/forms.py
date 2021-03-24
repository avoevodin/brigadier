from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Project, Task


class ProjectModelForm(forms.ModelForm):
    """todo()

    """

    class Meta:
        model = Project
        fields = ['project_name', 'deadline', 'budget', 'description']
        widgets = {
            'project_name': forms.TextInput(attrs={
                'class': 'form-control mb-2',
                'placeholder': _('Project name'),
            }),
            'deadline': forms.DateInput(attrs={
                'class': 'form-control mb-2',
                'placeholder': _('Deadline'),
            }),
            'budget': forms.NumberInput(attrs={
                'class': 'form-control mb-2',
                'placeholder': _('Budget'),
            }),
            'description': forms.TextInput(attrs={
                'class': 'form-control mb-2',
                'placeholder': _('Description'),
            })
        }


class TaskModelForm(forms.ModelForm):
    """todo()

    """

    class Meta:
        model = Task
        fields = [
            'project', 'task_name', 'start_date', 'complete_date',
            'author', 'executor', 'status', 'description'
        ]
        widgets = {
            'project': forms.Select(attrs={
                'class': 'form-select',
                'aria-label': 'Select a project',
            })
        }
