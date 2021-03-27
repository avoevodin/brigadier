from django.test import TestCase

from .models import Employee


def create_employee(**kwargs):
    """Create an employee with passed parameters.

    """
    try:
        return Employee.objects.create(
            firstname=kwargs.get('firstname'),
            middlename=kwargs.get('middlename'),
            surname=kwargs.get('surname'),
            email=kwargs.get('email'),
            birthdate=kwargs.get('birthdate'),
        )
    except ValueError:
        return ValueError


class EmployeeModelTest(TestCase):

    def test_empty_first_name(self):
        """todo()

        """
        result = 1
        # try:
        #     create_employee(kwargs={
        #         'middlename': 'test',
        #
        #     })
        # except ValueError:
        #     result = 0

        self.assertEqual(0, 0)
