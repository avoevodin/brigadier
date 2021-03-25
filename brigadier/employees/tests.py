from django.test import TestCase

from .models import Employee


def CreateEmployee(**kwargs):
    """Create an employee with passed parameters.

    """
    return Employee.objects.create(
        kwargs.get('firstname'),
        kwargs.get('middlename'),
        kwargs.get('surname'),
        kwargs.get('firstname'),
        kwargs.get('email'),
        kwargs.get('birthdate'),
    )
