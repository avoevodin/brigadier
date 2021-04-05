import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from django.utils.translation import gettext as _

from .models import Project, Task, Comment
from employees.tests import create_employee


def create_project(**kwargs):
    """todo

    """
    return Project.objects.create(
        project_name=kwargs.get('project_name'),
        description=kwargs.get('description'),
        budget=kwargs.get('budget'),
        deadline=kwargs.get('deadline'),
        closed=kwargs.get('closed'),
    )


def create_task(**kwargs):
    """todo

    """
    return Project.objects.create(
        project_name=kwargs.get('project_name'),
        description=kwargs.get('description'),
        budget=kwargs.get('budget'),
        deadline=kwargs.get('deadline'),
        closed=kwargs.get('closed'),
    )


class ProjectModelTest(TestCase):
    """todo

    """

    def test_model_str(self):
        """todo

        """
        postfix = '_1'
        project_str = create_project(**{
            'project_name': 'Project name' + postfix,
            'description': 'Project description' + postfix,
            'budget': 100000,
            'deadline': timezone.now() + datetime.timedelta(days=32),
            'closed': False,
        }).__str__()
        project_str_target = 'Project name_1'
        self.assertEqual(project_str, project_str_target)


class ProjectListViewTest(TestCase):
    """todo

    """

    def test_no_projects(self):
        """todo

        """
        response = self.client.get(reverse('projects:list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, _("No projects are available."))
        self.assertQuerysetEqual(response.context['project_list'], [])

    def test_two_projects_without_tasks(self):
        """todo

        """
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
        qs_target = [
            {
                'project_name': 'Project name 2',
                'deadline': deadline,
                'budget': 100000.0,
                'closed': False,
                'tasks_count': 0,
                'percentage_completed': 0.0
            },
            {
                'project_name': 'Project name 1',
                'deadline': deadline,
                'budget': 100000.0,
                'closed': False,
                'tasks_count': 0,
                'percentage_completed': 0.0
            }
        ]
        response = self.client.get(reverse('projects:list'))
        fields = list(response.context['project_list']._fields)
        fields.remove('id')
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['project_list'].values(*fields), qs_target, transform=lambda x: x)

    def test_two_projects_with_two_tasks(self):
        """todo

        """
        deadline = timezone.now() + datetime.timedelta(days=32)

        postfix = '_1'
        firstname = 'Marshall' + postfix
        middlename = 'Bruce' + postfix
        surname = 'Mathers' + postfix
        email = f'mbm{postfix}@example.com'
        birthdate = timezone.now() + datetime.timedelta(days=-365 * 30)
        employee = create_employee(**{
            'firstname': firstname,
            'middlename': middlename,
            'surname': surname,
            'email': email,
            'birthdate': birthdate,
        })

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
        qs_target = [
            {
                'project_name': 'Project name 2',
                'deadline': deadline,
                'budget': 100000.0,
                'closed': False,
                'tasks_count': 0,
                'percentage_completed': 0.0
            },
            {
                'project_name': 'Project name 1',
                'deadline': deadline,
                'budget': 100000.0,
                'closed': False,
                'tasks_count': 0,
                'percentage_completed': 0.0
            }
        ]
        response = self.client.get(reverse('projects:list'))
        fields = list(response.context['project_list']._fields)
        fields.remove('id')
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['project_list'].values(*fields), qs_target, transform=lambda x: x)
