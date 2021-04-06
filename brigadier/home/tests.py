import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from projects.models import Project, Task, NEW, COMPLETED, IN_PROGRESS

from projects.tests import create_project, create_task
from employees.tests import create_employee


class HomeViewTest(TestCase):
    """todo

    """

    def test_project_statistics(self):
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

    def test_project_statistics_without_any_project(self):
        """todo

        """
        response = self.client.get(reverse('home:home'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context['projects_statistics'].values(),
            [0, 0, 0, 0],
            transform=lambda x: x
        )
