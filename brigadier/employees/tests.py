import datetime

from django.test import TestCase
from django.utils import timezone
from django.utils.translation import gettext as _
from django.urls import reverse

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
        birthdate = timezone.now() + datetime.timedelta(days=-365 * 30)
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
        birthdate = timezone.now() + datetime.timedelta(days=-365 * 30)
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
        birthdate = timezone.now() + datetime.timedelta(days=-365 * 30)
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
        birthdate = timezone.now() + datetime.timedelta(days=-365 * 30)
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
        birthdate = timezone.now() + datetime.timedelta(days=-365 * 30)
        full_name = create_employee(**{
            'firstname': firstname,
            'middlename': middlename,
            'surname': surname,
            'email': email,
            'birthdate': birthdate,
        }).full_name()
        full_name_target = ''
        self.assertEqual(full_name, full_name_target)

    def test_model_str(self):
        """todo

        """
        firstname = 'Marshall'
        middlename = 'Bruce'
        surname = 'Mathers'
        email = 'mbm@example.com'
        birthdate = timezone.now() + datetime.timedelta(days=-365 * 30)
        employee_str = create_employee(**{
            'firstname': firstname,
            'middlename': middlename,
            'surname': surname,
            'email': email,
            'birthdate': birthdate,
        }).__str__()
        self.assertEqual(employee_str, 'Marshall Bruce Mathers')


class EmployeeListViewTest(TestCase):
    """todo

    """
    def test_no_employees(self):
        """todo

        """
        response = self.client.get(reverse('employees:list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, _("No employees are available."))
        self.assertQuerysetEqual(response.context['employee_list'], [])

    def test_two_employees(self):
        """todo

        """
        postfix = '_1'
        firstname = 'Marshall' + postfix
        middlename = 'Bruce' + postfix
        surname = 'Mathers' + postfix
        email = f'mbm{postfix}@example.com'
        birthdate = timezone.now() + datetime.timedelta(days=-365 * 30)
        create_employee(**{
            'firstname': firstname,
            'middlename': middlename,
            'surname': surname,
            'email': email,
            'birthdate': birthdate,
        })
        postfix = '_2'
        firstname = 'Marshall' + postfix
        middlename = 'Bruce' + postfix
        surname = 'Mathers' + postfix
        email = f'mbm{postfix}@example.com'
        birthdate = timezone.now() + datetime.timedelta(days=-365 * 30)
        create_employee(**{
            'firstname': firstname,
            'middlename': middlename,
            'surname': surname,
            'email': email,
            'birthdate': birthdate,
        })
        response = self.client.get(reverse('employees:list'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['employee_list'], ['<Employee: Marshall_1 Bruce_1 Mathers_1>',
                                                                     '<Employee: Marshall_2 Bruce_2 Mathers_2>'])


class EmployeeDetailViewTest(TestCase):
    """todo

    """
    def test_not_existed_employee(self):
        """todo

        """
        response = self.client.get(reverse('employees:detail', args=(1,)))
        self.assertEqual(response.status_code, 404)
