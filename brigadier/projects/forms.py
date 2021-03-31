from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Project, Task


class ProjectModelForm(forms.ModelForm):
    """Class describes the model form of the Project
    class.

    """

    class Meta:
        model = Project
        fields = ['project_name', 'deadline', 'budget', 'closed', 'description']
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
    """Class describes the model form of the
    Task class.

    """

    class Meta:
        model = Task
        fields = [
            'project', 'task_name', 'start_date', 'complete_date',
            'author', 'assignee', 'status', 'description'
        ]
        widgets = {
            'project': forms.Select(attrs={
                'class': 'form-select mb-2',
            }),
            'task_name': forms.TextInput(attrs={
                'class': 'form-control mb-2',
                'placeholder': _('Task name')
            }),
            'start_date': forms.DateTimeInput(attrs={
                'class': 'form-control mb-2',
                'placeholder': _('Start date'),
            }),
            'complete_date': forms.DateTimeInput(attrs={
                'class': 'form-control mb-2',
                'placeholder': _('Complete date'),
            }),
            'author': forms.Select(attrs={
                'class': 'form-select mb-2',
            }),
            'assignee': forms.Select(attrs={
                'class': 'form-select mb-2',
            }),
            'status': forms.Select(attrs={
                'class': 'form-select mb-2',
            }),
            'description': forms.TextInput(attrs={
                'class': 'form-control mb-2',
                'placeholder': _('Description')
            }),
        }
