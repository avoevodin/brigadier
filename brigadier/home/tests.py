import datetime

from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from employees.tests import create_employee
from projects.models import NEW, COMPLETED, IN_PROGRESS
from projects.tests import create_project, create_task

User = get_user_model()


class HomeViewTest(TestCase):
    """Tests for home page view.

    """
    def test_statistics_without_any_object(self):
        """Test home page statistics without any objects of Project,
        Task and Employee.

        """
        username = 'test'
        email = 'user@example.com'
        password = 'test'
        usr = User.objects.create_user(username=username, password=password, email=email, )
        usr.groups.add(Group.objects.get(name='public'))
        self.client.login(username=username, password=password)

        response = self.client.get(reverse('home:home'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context['projects_statistics'].values(),
            [0, 0, 0, 0],
            transform=lambda x: x
        )
        self.assertQuerysetEqual(
            response.context['tasks_statistics'].values(),
            [0, 0, 0, 0, 0],
            transform=lambda x: x
        )
        self.assertQuerysetEqual(
            response.context['employees_statistics'].values(),
            [0, 0, 0, 0],
            transform=lambda x: x
        )

    def test_project_statistics(self):
        """Test projects statistics of home page.

        """
        username = 'test'
        email = 'user@example.com'
        password = 'test'
        usr = User.objects.create_user(username=username, password=password, email=email, )
        usr.groups.add(Group.objects.get(name='public'))
        self.client.login(username=username, password=password)

        deadline = timezone.now() + datetime.timedelta(days=32)
        postfix = ' 1'
        create_project(**{
            'project_name': 'Project name' + postfix,
            'description': 'Project description' + postfix,
            'budget': 100000,
            'deadline': deadline,
            'closed': False,
        })
        postfix = ' 2'
        create_project(**{
            'project_name': 'Project name' + postfix,
            'description': 'Project description' + postfix,
            'budget': 100000,
            'deadline': deadline,
            'closed': False,
        })
        deadline = timezone.now() + datetime.timedelta(days=-30)
        postfix = ' 3'
        create_project(**{
            'project_name': 'Project name' + postfix,
            'description': 'Project description' + postfix,
            'budget': 100000,
            'deadline': deadline,
            'closed': True,
        })
        deadline = timezone.now() + datetime.timedelta(days=-1)
        postfix = ' 4'
        create_project(**{
            'project_name': 'Project name' + postfix,
            'description': 'Project description' + postfix,
            'budget': 100000,
            'deadline': deadline,
            'closed': False,
        })
        response = self.client.get(reverse('home:home'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context['projects_statistics'].values(),
            [4, 3, 1, 1],
            transform=lambda x: x
        )

    def test_task_statistics(self):
        """Test tasks statistics of home page view.

        """
        username = 'test'
        email = 'user@example.com'
        password = 'test'
        usr = User.objects.create_user(username=username, password=password, email=email, )
        usr.groups.add(Group.objects.get(name='public'))
        self.client.login(username=username, password=password)

        deadline = timezone.now() + datetime.timedelta(days=32)
        postfix = ' 1'
        project_1 = create_project(**{
            'project_name': 'Project name' + postfix,
            'description': 'Project description' + postfix,
            'budget': 100000,
            'deadline': deadline,
            'closed': False,
        })

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

        postfix = ' 1'
        start_date = timezone.now()
        complete_date = timezone.now() + datetime.timedelta(days=8)
        create_task(**{
            'project': project_1,
            'task_name': 'Task name' + postfix,
            'description': 'description',
            'start_date': start_date,
            'complete_date': complete_date,
            'author': employee_1,
            'assignee': employee_1,
            'status': NEW,
        })
        postfix = ' 2'
        start_date = timezone.now() + datetime.timedelta(days=4)
        complete_date = timezone.now() + datetime.timedelta(days=8)
        create_task(**{
            'project': project_1,
            'task_name': 'Task name' + postfix,
            'description': 'description',
            'start_date': start_date,
            'complete_date': complete_date,
            'author': employee_1,
            'assignee': employee_1,
            'status': NEW,
        })
        postfix = ' 3'
        start_date = timezone.now() + datetime.timedelta(days=-4)
        complete_date = timezone.now() + datetime.timedelta(days=8)
        create_task(**{
            'project': project_1,
            'task_name': 'Task name' + postfix,
            'description': 'description',
            'start_date': start_date,
            'complete_date': complete_date,
            'author': employee_1,
            'assignee': employee_1,
            'status': NEW,
        })
        postfix = ' 4'
        start_date = timezone.now() + datetime.timedelta(days=-14)
        complete_date = timezone.now() + datetime.timedelta(days=-6)
        create_task(**{
            'project': project_1,
            'task_name': 'Task name' + postfix,
            'description': 'description',
            'start_date': start_date,
            'complete_date': complete_date,
            'author': employee_1,
            'assignee': employee_1,
            'status': NEW,
        })
        postfix = ' 5'
        start_date = timezone.now() + datetime.timedelta(days=-4)
        complete_date = timezone.now() + datetime.timedelta(days=10)
        create_task(**{
            'project': project_1,
            'task_name': 'Task name' + postfix,
            'description': 'description',
            'start_date': start_date,
            'complete_date': complete_date,
            'author': employee_1,
            'assignee': employee_1,
            'status': IN_PROGRESS,
        })
        postfix = ' 6'
        start_date = timezone.now() + datetime.timedelta(days=-8)
        complete_date = timezone.now() + datetime.timedelta(days=-4)
        create_task(**{
            'project': project_1,
            'task_name': 'Task name' + postfix,
            'description': 'description',
            'start_date': start_date,
            'complete_date': complete_date,
            'author': employee_1,
            'assignee': employee_1,
            'status': IN_PROGRESS,
        })
        postfix = ' 7'
        start_date = timezone.now() + datetime.timedelta(days=8)
        complete_date = timezone.now() + datetime.timedelta(days=14)
        create_task(**{
            'project': project_1,
            'task_name': 'Task name' + postfix,
            'description': 'description',
            'start_date': start_date,
            'complete_date': complete_date,
            'author': employee_1,
            'assignee': employee_1,
            'status': IN_PROGRESS,
        })
        postfix = ' 8'
        start_date = timezone.now() + datetime.timedelta(days=8)
        complete_date = timezone.now() + datetime.timedelta(days=14)
        create_task(**{
            'project': project_1,
            'task_name': 'Task name' + postfix,
            'description': 'description',
            'start_date': start_date,
            'complete_date': complete_date,
            'author': employee_1,
            'assignee': employee_1,
            'status': COMPLETED,
        })
        postfix = ' 9'
        start_date = timezone.now() + datetime.timedelta(days=-8)
        complete_date = timezone.now() + datetime.timedelta(days=14)
        create_task(**{
            'project': project_1,
            'task_name': 'Task name' + postfix,
            'description': 'description',
            'start_date': start_date,
            'complete_date': complete_date,
            'author': employee_1,
            'assignee': employee_1,
            'status': COMPLETED,
        })
        postfix = ' 10'
        start_date = timezone.now() + datetime.timedelta(days=-14)
        complete_date = timezone.now() + datetime.timedelta(days=-6)
        create_task(**{
            'project': project_1,
            'task_name': 'Task name' + postfix,
            'description': 'description',
            'start_date': start_date,
            'complete_date': complete_date,
            'author': employee_1,
            'assignee': employee_1,
            'status': COMPLETED,
        })
        response = self.client.get(reverse('home:home'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context['tasks_statistics'].values(),
            [10, 2, 1, 3, 4],
            transform=lambda x: x
        )

    def test_employee_statistics(self):
        """Test employees statistics of home page view.

        """
        username = 'test'
        email = 'user@example.com'
        password = 'test'
        usr = User.objects.create_user(username=username, password=password, email=email, )
        usr.groups.add(Group.objects.get(name='public'))

        self.client.login(username=username, password=password)

        deadline = timezone.now() + datetime.timedelta(days=32)
        postfix = ' 1'
        project_1 = create_project(**{
            'project_name': 'Project name' + postfix,
            'description': 'Project description' + postfix,
            'budget': 100000,
            'deadline': deadline,
            'closed': False,
        })

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
        employee_2 = create_employee(**{
            'firstname': firstname,
            'middlename': middlename,
            'surname': surname,
            'email': email,
            'birthdate': birthdate,
        })
        postfix = '_3'
        firstname = 'Marshall' + postfix
        middlename = 'Bruce' + postfix
        surname = 'Mathers' + postfix
        email = f'mbm{postfix}@example.com'
        birthdate = timezone.now() + datetime.timedelta(days=-365 * 30)
        employee_3 = create_employee(**{
            'firstname': firstname,
            'middlename': middlename,
            'surname': surname,
            'email': email,
            'birthdate': birthdate,
        })
        postfix = '_4'
        firstname = 'Marshall' + postfix
        middlename = 'Bruce' + postfix
        surname = 'Mathers' + postfix
        email = f'mbm{postfix}@example.com'
        birthdate = timezone.now() + datetime.timedelta(days=-365 * 30)
        employee_4 = create_employee(**{
            'firstname': firstname,
            'middlename': middlename,
            'surname': surname,
            'email': email,
            'birthdate': birthdate,
        })
        postfix = '_5'
        firstname = 'Marshall' + postfix
        middlename = 'Bruce' + postfix
        surname = 'Mathers' + postfix
        email = f'mbm{postfix}@example.com'
        birthdate = timezone.now() + datetime.timedelta(days=-365 * 30)
        employee_5 = create_employee(**{
            'firstname': firstname,
            'middlename': middlename,
            'surname': surname,
            'email': email,
            'birthdate': birthdate,
        })
        postfix = '_6'
        firstname = 'Marshall' + postfix
        middlename = 'Bruce' + postfix
        surname = 'Mathers' + postfix
        email = f'mbm{postfix}@example.com'
        birthdate = timezone.now() + datetime.timedelta(days=-365 * 30)
        employee_6 = create_employee(**{
            'firstname': firstname,
            'middlename': middlename,
            'surname': surname,
            'email': email,
            'birthdate': birthdate,
        })
        postfix = '_7'
        firstname = 'Marshall' + postfix
        middlename = 'Bruce' + postfix
        surname = 'Mathers' + postfix
        email = f'mbm{postfix}@example.com'
        birthdate = timezone.now() + datetime.timedelta(days=-365 * 30)
        employee_7 = create_employee(**{
            'firstname': firstname,
            'middlename': middlename,
            'surname': surname,
            'email': email,
            'birthdate': birthdate,
        })
        postfix = '_8'
        firstname = 'Marshall' + postfix
        middlename = 'Bruce' + postfix
        surname = 'Mathers' + postfix
        email = f'mbm{postfix}@example.com'
        birthdate = timezone.now() + datetime.timedelta(days=-365 * 30)
        employee_8 = create_employee(**{
            'firstname': firstname,
            'middlename': middlename,
            'surname': surname,
            'email': email,
            'birthdate': birthdate,
        })
        postfix = '_9'
        firstname = 'Marshall' + postfix
        middlename = 'Bruce' + postfix
        surname = 'Mathers' + postfix
        email = f'mbm{postfix}@example.com'
        birthdate = timezone.now() + datetime.timedelta(days=-365 * 30)
        employee_9 = create_employee(**{
            'firstname': firstname,
            'middlename': middlename,
            'surname': surname,
            'email': email,
            'birthdate': birthdate,
        })
        postfix = '_10'
        firstname = 'Marshall' + postfix
        middlename = 'Bruce' + postfix
        surname = 'Mathers' + postfix
        email = f'mbm{postfix}@example.com'
        birthdate = timezone.now() + datetime.timedelta(days=-365 * 30)
        employee_10 = create_employee(**{
            'firstname': firstname,
            'middlename': middlename,
            'surname': surname,
            'email': email,
            'birthdate': birthdate,
        })

        postfix = ' 1'
        start_date = timezone.now()
        complete_date = timezone.now() + datetime.timedelta(days=8)
        create_task(**{
            'project': project_1,
            'task_name': 'Task name' + postfix,
            'description': 'description',
            'start_date': start_date,
            'complete_date': complete_date,
            'author': employee_1,
            'assignee': employee_2,
            'status': NEW,
        })
        postfix = ' 2'
        start_date = timezone.now() + datetime.timedelta(days=4)
        complete_date = timezone.now() + datetime.timedelta(days=8)
        create_task(**{
            'project': project_1,
            'task_name': 'Task name' + postfix,
            'description': 'description',
            'start_date': start_date,
            'complete_date': complete_date,
            'author': employee_1,
            'assignee': employee_2,
            'status': NEW,
        })
        postfix = ' 3'
        start_date = timezone.now() + datetime.timedelta(days=-4)
        complete_date = timezone.now() + datetime.timedelta(days=8)
        create_task(**{
            'project': project_1,
            'task_name': 'Task name' + postfix,
            'description': 'description',
            'start_date': start_date,
            'complete_date': complete_date,
            'author': employee_1,
            'assignee': employee_3,
            'status': NEW,
        })
        postfix = ' 4'
        start_date = timezone.now() + datetime.timedelta(days=-14)
        complete_date = timezone.now() + datetime.timedelta(days=-6)
        create_task(**{
            'project': project_1,
            'task_name': 'Task name' + postfix,
            'description': 'description',
            'start_date': start_date,
            'complete_date': complete_date,
            'author': employee_1,
            'assignee': employee_4,
            'status': NEW,
        })
        postfix = ' 5'
        start_date = timezone.now() + datetime.timedelta(days=-4)
        complete_date = timezone.now() + datetime.timedelta(days=10)
        create_task(**{
            'project': project_1,
            'task_name': 'Task name' + postfix,
            'description': 'description',
            'start_date': start_date,
            'complete_date': complete_date,
            'author': employee_1,
            'assignee': employee_4,
            'status': IN_PROGRESS,
        })
        postfix = ' 6'
        start_date = timezone.now() + datetime.timedelta(days=-8)
        complete_date = timezone.now() + datetime.timedelta(days=-4)
        create_task(**{
            'project': project_1,
            'task_name': 'Task name' + postfix,
            'description': 'description',
            'start_date': start_date,
            'complete_date': complete_date,
            'author': employee_1,
            'assignee': employee_2,
            'status': IN_PROGRESS,
        })
        postfix = ' 7'
        start_date = timezone.now() + datetime.timedelta(days=8)
        complete_date = timezone.now() + datetime.timedelta(days=14)
        create_task(**{
            'project': project_1,
            'task_name': 'Task name' + postfix,
            'description': 'description',
            'start_date': start_date,
            'complete_date': complete_date,
            'author': employee_1,
            'assignee': employee_5,
            'status': IN_PROGRESS,
        })
        postfix = ' 8'
        start_date = timezone.now() + datetime.timedelta(days=8)
        complete_date = timezone.now() + datetime.timedelta(days=14)
        create_task(**{
            'project': project_1,
            'task_name': 'Task name' + postfix,
            'description': 'description',
            'start_date': start_date,
            'complete_date': complete_date,
            'author': employee_1,
            'assignee': employee_6,
            'status': COMPLETED,
        })
        postfix = ' 9'
        start_date = timezone.now() + datetime.timedelta(days=-8)
        complete_date = timezone.now() + datetime.timedelta(days=14)
        create_task(**{
            'project': project_1,
            'task_name': 'Task name' + postfix,
            'description': 'description',
            'start_date': start_date,
            'complete_date': complete_date,
            'author': employee_1,
            'assignee': employee_7,
            'status': COMPLETED,
        })
        postfix = ' 10'
        start_date = timezone.now() + datetime.timedelta(days=-14)
        complete_date = timezone.now() + datetime.timedelta(days=-6)
        create_task(**{
            'project': project_1,
            'task_name': 'Task name' + postfix,
            'description': 'description',
            'start_date': start_date,
            'complete_date': complete_date,
            'author': employee_1,
            'assignee': employee_8,
            'status': COMPLETED,
        })
        postfix = ' 11'
        start_date = timezone.now() + datetime.timedelta(days=-24)
        complete_date = timezone.now() + datetime.timedelta(days=-1)
        create_task(**{
            'project': project_1,
            'task_name': 'Task name' + postfix,
            'description': 'description',
            'start_date': start_date,
            'complete_date': complete_date,
            'author': employee_1,
            'assignee': employee_9,
            'status': IN_PROGRESS,
        })
        postfix = ' 11'
        start_date = timezone.now() + datetime.timedelta(days=-21)
        complete_date = timezone.now() + datetime.timedelta(days=-2)
        create_task(**{
            'project': project_1,
            'task_name': 'Task name' + postfix,
            'description': 'description',
            'start_date': start_date,
            'complete_date': complete_date,
            'author': employee_1,
            'assignee': employee_4,
            'status': IN_PROGRESS,
        })
        postfix = ' 12'
        start_date = timezone.now() + datetime.timedelta(days=4)
        complete_date = timezone.now() + datetime.timedelta(days=6)
        create_task(**{
            'project': project_1,
            'task_name': 'Task name' + postfix,
            'description': 'description',
            'start_date': start_date,
            'complete_date': complete_date,
            'author': employee_1,
            'assignee': employee_3,
            'status': IN_PROGRESS,
        })
        postfix = ' 13'
        start_date = timezone.now() + datetime.timedelta(days=-3)
        complete_date = timezone.now() + datetime.timedelta(days=8)
        create_task(**{
            'project': project_1,
            'task_name': 'Task name' + postfix,
            'description': 'description',
            'start_date': start_date,
            'complete_date': complete_date,
            'author': employee_1,
            'assignee': employee_7,
            'status': IN_PROGRESS,
        })
        response = self.client.get(reverse('home:home'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context['employees_statistics'].values(),
            [10, 4, 3, 6],
            transform=lambda x: x
        )
