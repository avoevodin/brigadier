import datetime

from django.test import TestCase
from django.utils import timezone
from django.utils.translation import gettext as _
from django.urls import reverse
from django.contrib.auth.models import Permission
from django.contrib.auth import get_user_model

from .models import Employee

User = get_user_model()

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
    """Tests for Employee model.

    """
    def test_full_name(self):
        """Test full name representation of employee with selected firstname,
        middlename and surname.

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
        """Test full name representation of employee with selected
        middlename and surname.

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
        """Test full name representation of employee with selected firstname,
        and surname.

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
        """Test full name representation of employee with selected firstname and
        middlename.

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
        """Test full name representation without any name.

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
        """Test model __str__ representation.

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
    """Test for list view of Employee model.

    """

    def test_no_employees(self):
        """Test for list view without any employee.

        """
        username = 'test'
        email = 'user@example.com'
        password = 'test'
        perms = Permission.objects.filter(codename__in=['view_employee'])
        usr = User.objects.create_user(username=username, password=password, email=email, )
        usr.user_permissions.set(perms)
        self.client.login(username=username, password=password)

        response = self.client.get(reverse('employees:list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, _("No employees are available."))
        self.assertQuerysetEqual(response.context['employee_list'], [])

    def test_two_employees(self):
        """Test for list view with two employees.

        """
        username = 'test'
        email = 'user@example.com'
        password = 'test'
        perms = Permission.objects.filter(codename__in=['view_employee'])
        usr = User.objects.create_user(username=username, password=password, email=email, )
        usr.user_permissions.set(perms)
        self.client.login(username=username, password=password)

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
    """Tests for detail view of Employee model.

    """
    def test_not_existed_employee(self):
        """Test for detail view of not existed employee.

        """
        username = 'test'
        email = 'user@example.com'
        password = 'test'
        perms = Permission.objects.filter(codename__in=['view_employee'])
        usr = User.objects.create_user(username=username, password=password, email=email,)
        usr.user_permissions.set(perms)
        self.client.login(username=username, password=password)

        response = self.client.get(reverse('employees:detail', args=(1,)))
        self.assertEqual(response.status_code, 404)


class EmployeeCreateViewTest(TestCase):
    """Tests for Employee create view.

    """
    def test_create_employee_without_login(self):
        """Test of creating employee without login.

        """
        postfix = '_1'
        firstname = 'Marshall' + postfix
        middlename = 'Bruce' + postfix
        surname = 'Mathers' + postfix
        email = f'mbm{postfix}@example.com'
        birthdate = timezone.now() + datetime.timedelta(days=-365 * 30)
        response = self.client.post(
            reverse('employees:create'),
            {
                'firstname': firstname,
                'middlename': middlename,
                'surname': surname,
                'email': email,
                'birthdate': birthdate.strftime("%m/%d/%Y"),
            }
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/accounts/login/?next=/employees/add/')

    def test_create_employee_without_perms(self):
        """Test of creating employee.

        """
        username = 'test'
        email = 'user@example.com'
        password = 'test'
        User.objects.create_user(username=username, password=password, email=email,)
        self.client.login(username=username, password=password)

        postfix = '_1'
        firstname = 'Marshall' + postfix
        middlename = 'Bruce' + postfix
        surname = 'Mathers' + postfix
        email = f'mbm{postfix}@example.com'
        birthdate = timezone.now() + datetime.timedelta(days=-365 * 30)
        response = self.client.post(
            reverse('employees:create'),
            {
                'firstname': firstname,
                'middlename': middlename,
                'surname': surname,
                'email': email,
                'birthdate': birthdate.strftime("%m/%d/%Y"),
            }
        )
        self.assertEqual(response.status_code, 403)

    def test_create_employee(self):
        """Test of creating employee.

        """
        username = 'test'
        email = 'user@example.com'
        password = 'test'
        perms = Permission.objects.filter(codename__in=['view_employee', 'add_employee'])
        usr = User.objects.create_user(username=username, password=password, email=email,)
        usr.user_permissions.set(perms)
        self.client.login(username=username, password=password)

        postfix = '_1'
        firstname = 'Marshall' + postfix
        middlename = 'Bruce' + postfix
        surname = 'Mathers' + postfix
        email = f'mbm{postfix}@example.com'
        birthdate = timezone.now() + datetime.timedelta(days=-365 * 30)
        response = self.client.post(
            reverse('employees:create'),
            {
                'firstname': firstname,
                'middlename': middlename,
                'surname': surname,
                'email': email,
                'birthdate': birthdate.strftime("%m/%d/%Y"),
            }
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('employees:list'))

        response = self.client.get(response.url)
        self.assertQuerysetEqual(response.context['employee_list'], ['<Employee: Marshall_1 Bruce_1 Mathers_1>'])


class EmployeeEditViewTest(TestCase):
    """Test for Employee edit view.

    """
    def test_edit_employee_without_next(self):
        """Test editing of Employee without next-hook.

        """
        username = 'test'
        email = 'user@example.com'
        password = 'test'
        perms = Permission.objects.filter(codename__in=['change_employee', 'view_employee'])
        usr = User.objects.create_user(username=username, password=password, email=email, )
        usr.user_permissions.set(perms)
        self.client.login(username=username, password=password)

        postfix = '_1'
        firstname = 'Marshall' + postfix
        middlename = 'Bruce' + postfix
        surname = 'Mathers' + postfix
        email = f'mbm{postfix}@example.com'
        birthdate = timezone.now() + datetime.timedelta(days=-365 * 30)
        employee_1 = create_employee(**{
            'firstname': firstname,
            'middlename': middlename,
            'surname': surname,
            'email': email,
            'birthdate': birthdate,
        })
        response = self.client.post(
            reverse('employees:edit', args=(employee_1.id,)),
            {
                'firstname': firstname + ' New',
                'middlename': middlename,
                'surname': surname,
                'email': email,
                'birthdate': birthdate.strftime("%m/%d/%Y"),
            }
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('employees:list'))

        response = self.client.get(response.url)
        self.assertQuerysetEqual(
            response.context['employee_list'],
            ['<Employee: Marshall_1 New Bruce_1 Mathers_1>']
        )

    def test_edit_employee_with_next(self):
        """Test editing of Employee with next-hook

        """
        username = 'test'
        email = 'user@example.com'
        password = 'test'
        perms = Permission.objects.filter(codename__in=['change_employee', 'view_employee'])
        usr = User.objects.create_user(username=username, password=password, email=email,)
        usr.user_permissions.set(perms)
        self.client.login(username=username, password=password)

        postfix = '_1'
        firstname = 'Marshall' + postfix
        middlename = 'Bruce' + postfix
        surname = 'Mathers' + postfix
        email = f'mbm{postfix}@example.com'
        birthdate = timezone.now() + datetime.timedelta(days=-365 * 30)
        employee_1 = create_employee(**{
            'firstname': firstname,
            'middlename': middlename,
            'surname': surname,
            'email': email,
            'birthdate': birthdate,
        })
        next_url = reverse('employees:detail', args=(employee_1.id,))
        response = self.client.post(
            reverse('employees:edit', args=(employee_1.id,)) + "?next=" + next_url,
            {
                'firstname': firstname + ' New',
                'middlename': middlename,
                'surname': surname,
                'email': email,
                'birthdate': birthdate.strftime("%m/%d/%Y"),
            }
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, next_url)

        response = self.client.get(response.url)
        self.assertQuerysetEqual(
            response.context['employee'].firstname,
            'Marshall_1 New',
            transform=lambda x: x
        )


class EmployeeDeleteViewTest(TestCase):
    """Tests for delete view of Employee model.

    """
    def test_delete_employee_with_next(self):
        """Test deleting employee with next-hook.

        """
        username = 'test'
        email = 'user@example.com'
        password = 'test'
        perms = Permission.objects.filter(codename__in=['delete_employee', 'view_employee'])
        usr = User.objects.create_user(username=username, password=password, email=email, )
        usr.user_permissions.set(perms)
        self.client.login(username=username, password=password)

        postfix = '_1'
        firstname = 'Marshall' + postfix
        middlename = 'Bruce' + postfix
        surname = 'Mathers' + postfix
        email = f'mbm{postfix}@example.com'
        birthdate = timezone.now() + datetime.timedelta(days=-365 * 30)
        employee_1 = create_employee(**{
            'firstname': firstname,
            'middlename': middlename,
            'surname': surname,
            'email': email,
            'birthdate': birthdate,
        })
        next_url = reverse('employees:detail', args=(employee_1.id,))
        response = self.client.post(
            reverse('employees:delete', args=(employee_1.id,)) + "?next=" + next_url,
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('employees:list'))

        response = self.client.get(response.url)
        self.assertContains(response, _("No employees are available."))
        self.assertQuerysetEqual(
            response.context['employee_list'],
            []
        )

    def test_delete_employee_without_next(self):
        """Test deleting of employee without next-hook.

        """
        username = 'test'
        email = 'user@example.com'
        password = 'test'
        perms = Permission.objects.filter(codename__in=['delete_employee', 'view_employee'])
        usr = User.objects.create_user(username=username, password=password, email=email,)
        usr.user_permissions.set(perms)
        self.client.login(username=username, password=password)

        postfix = '_1'
        firstname = 'Marshall' + postfix
        middlename = 'Bruce' + postfix
        surname = 'Mathers' + postfix
        email = f'mbm{postfix}@example.com'
        birthdate = timezone.now() + datetime.timedelta(days=-365 * 30)
        employee_1 = create_employee(**{
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
        response = self.client.post(
            reverse('employees:delete', args=(employee_1.id,)),
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('employees:list'))

        response = self.client.get(response.url)
        self.assertQuerysetEqual(
            response.context['employee_list'],
            ['<Employee: Marshall_2 Bruce_2 Mathers_2>']
        )
