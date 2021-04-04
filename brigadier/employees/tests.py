import datetime

from django.test import TestCase
from django.utils import timezone

from .models import Employee


def create_employee(**kwargs):
    """Create an employee with passed parameters.

    """
    return Employee.objects.create(
        firstname=kwargs.get('firstname'),
        middlename=kwargs.get('middlename'),
        surname=kwargs.get('surname'),
        email=kwargs.get('email'),
        birthdate=kwargs.get('birthdate'),
    )


class EmployeeModelTest(TestCase):

    def test_full_name(self):
        """todo

        """
        firstname = 'Marshall'
        middlename = 'Bruce'
        surname = 'Mathers'
        email = 'mbm@example.com'
        birthdate = timezone.now()
        full_name = create_employee(**{
            'firstname': firstname,
            'middlename': middlename,
            'surname': surname,
            'email': email,
            'birthdate': birthdate,
        }).full_name()
        full_name_target = 'Marshall Bruce Mathers'
        self.assertEqual(full_name, full_name_target)

    def test_full_name_without_firstname(self):
        """todo

        """
        firstname = ''
        middlename = 'Bruce'
        surname = 'Mathers'
        email = 'mbm@example.com'
        birthdate = timezone.now()
        full_name = create_employee(**{
            'firstname': firstname,
            'middlename': middlename,
            'surname': surname,
            'email': email,
            'birthdate': birthdate,
        }).full_name()
        full_name_target = 'Bruce Mathers'
        self.assertEqual(full_name, full_name_target)

    def test_full_name_without_middlename(self):
        """todo

        """
        firstname = 'Marshall'
        middlename = None
        surname = 'Mathers'
        email = 'mbm@example.com'
        birthdate = timezone.now()
        full_name = create_employee(**{
            'firstname': firstname,
            'middlename': middlename,
            'surname': surname,
            'email': email,
            'birthdate': birthdate,
        }).full_name()
        full_name_target = 'Marshall Mathers'
        self.assertEqual(full_name, full_name_target)

    def test_full_name_without_surname(self):
        """todo

        """
        firstname = 'Marshall'
        middlename = 'Bruce'
        surname = ''
        email = 'mbm@example.com'
        birthdate = timezone.now()
        full_name = create_employee(**{
            'firstname': firstname,
            'middlename': middlename,
            'surname': surname,
            'email': email,
            'birthdate': birthdate,
        }).full_name()
        full_name_target = " ".join([firstname or '', middlename or '', surname or '']) \
            .replace("  ", " ").strip()
        self.assertEqual(full_name, full_name_target)

    def test_full_name_without_any_name(self):
        """todo

        """
        firstname = ''
        middlename = None
        surname = ''
        email = 'mbm@example.com'
        birthdate = timezone.now()
        full_name = create_employee(**{
            'firstname': firstname,
            'middlename': middlename,
            'surname': surname,
            'email': email,
            'birthdate': birthdate,
        }).full_name()
        full_name_target = ''
        self.assertEqual(full_name, full_name_target)