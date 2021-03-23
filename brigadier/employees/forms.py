from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Employee


class EmployeeModelForm(forms.ModelForm):
    """Class for creating and rendering form,
    validating a form, passing a signal for saving data.
    It's connected to model Employee (which performs updating
    and inserting).

    """
    class Meta:
        model = Employee
        fields = ['firstname', 'middlename', 'surname', 'email', 'birthdate']
        widgets = {
            'firstname': forms.TextInput(attrs={
                'class': 'form-control mb-2',
                'placeholder': _('Firstname'),
            }),
            'middlename': forms.TextInput(attrs={
                'class': 'form-control mb-2',
                'placeholder': _('Middlename'),
            }),
            'surname': forms.TextInput(attrs={
                'class': 'form-control mb-2',
                'placeholder': _('Surname'),
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control mb-2',
                'placeholder': _('Email'),
            }),
            'birthdate': forms.DateInput(attrs={
                'class': 'form-control mb-2',
                'placeholder': _('Birthdate'),
            }),
        }
