from django import forms

from .models import Employee


class EmployeeModelForm(forms.ModelForm):
    """
    todo()
    """
    class Meta:
        model = Employee
        fields = ['firstname', 'middlename', 'surname', 'email', 'birthdate']
