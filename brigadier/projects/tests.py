import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from django.utils.translation import gettext as _

from .models import Project, Task, Comment, NEW, COMPLETED, IN_PROGRESS
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
    return Task.objects.create(
        project=kwargs.get('project'),
        task_name=kwargs.get('task_name'),
        description=kwargs.get('description'),
        start_date=kwargs.get('start_date'),
        complete_date=kwargs.get('complete_date'),
        author=kwargs.get('author'),
        assignee=kwargs.get('author'),
        status=kwargs.get('status'),
    )


def create_comment(**kwargs):
    """todo

    """
    return Comment.objects.create(
        task=kwargs.get('task'),
        text=kwargs.get('text'),
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
                'project_name': 'Project name 1',
                'deadline': deadline,
                'budget': 100000.0,
                'closed': False,
                'tasks_count': 0,
                'percentage_completed': 0.0
            },
            {
                'project_name': 'Project name 2',
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
        self.assertQuerysetEqual(response.context['project_list'].values(*fields).order_by('id'), qs_target,
                                 transform=lambda x: x)

    def test_three_projects_with_zero_one_two_tasks(self):
        """todo

        """
        deadline = timezone.now() + datetime.timedelta(days=32)
        start_date = timezone.now()
        complete_date = timezone.now() + datetime.timedelta(days=8)

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
        project_2 = create_project(**{
            'project_name': 'Project name' + postfix,
            'description': 'Project description' + postfix,
            'budget': 100000,
            'deadline': deadline,
            'closed': False,
        })
        postfix = ' 3'
        project_3 = create_project(**{
            'project_name': 'Project name' + postfix,
            'description': 'Project description' + postfix,
            'budget': 100000,
            'deadline': deadline,
            'closed': False,
        })
        postfix = ' 1'
        task_2_1 = create_task(**{
            'project': project_2,
            'task_name': 'Task name' + postfix,
            'description': 'description',
            'start_date': start_date,
            'complete_date': complete_date,
            'author': employee,
            'assignee': employee,
            'status': NEW,
        })
        postfix = ' 2'
        task_3_1 = create_task(**{
            'project': project_3,
            'task_name': 'Task name' + postfix,
            'description': 'description',
            'start_date': start_date,
            'complete_date': complete_date,
            'author': employee,
            'assignee': employee,
            'status': NEW,
        })
        postfix = ' 3'
        task_3_2 = create_task(**{
            'project': project_3,
            'task_name': 'Task name' + postfix,
            'description': 'description',
            'start_date': start_date,
            'complete_date': complete_date,
            'author': employee,
            'assignee': employee,
            'status': NEW,
        })

        qs_target = [
            {
                'project_name': 'Project name 1',
                'deadline': deadline,
                'budget': 100000.0,
                'closed': False,
                'tasks_count': 0,
                'percentage_completed': 0.0
            },
            {
                'project_name': 'Project name 2',
                'deadline': deadline,
                'budget': 100000.0,
                'closed': False,
                'tasks_count': 1,
                'percentage_completed': 0.0
            },
            {
                'project_name': 'Project name 3',
                'deadline': deadline,
                'budget': 100000.0,
                'closed': False,
                'tasks_count': 2,
                'percentage_completed': 0.0
            },
        ]
        response = self.client.get(reverse('projects:list'))
        fields = list(response.context['project_list']._fields)
        fields.remove('id')
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context['project_list'].values(*fields).order_by('id'),
            qs_target,
            transform=lambda x: x
        )

    def test_three_projects_percentage_completed(self):
        """todo

        """
        deadline = timezone.now() + datetime.timedelta(days=32)

        postfix = '_1'
        start_date = timezone.now()
        complete_date = timezone.now() + datetime.timedelta(days=8)
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
        project_1 = create_project(**{
            'project_name': 'Project name' + postfix,
            'description': 'Project description' + postfix,
            'budget': 100000,
            'deadline': deadline,
            'closed': True,
        })
        postfix = ' 2'
        project_2 = create_project(**{
            'project_name': 'Project name' + postfix,
            'description': 'Project description' + postfix,
            'budget': 100000,
            'deadline': deadline,
            'closed': False,
        })
        postfix = ' 3'
        project_3 = create_project(**{
            'project_name': 'Project name' + postfix,
            'description': 'Project description' + postfix,
            'budget': 100000,
            'deadline': deadline,
            'closed': False,
        })
        postfix = ' 1'
        task_2_1 = create_task(**{
            'project': project_2,
            'task_name': 'Task name' + postfix,
            'description': 'description',
            'start_date': start_date,
            'complete_date': complete_date,
            'author': employee,
            'assignee': employee,
            'status': NEW,
        })
        postfix = ' 2'
        task_3_1 = create_task(**{
            'project': project_3,
            'task_name': 'Task name' + postfix,
            'description': 'description',
            'start_date': start_date,
            'complete_date': complete_date,
            'author': employee,
            'assignee': employee,
            'status': NEW,
        })
        postfix = ' 3'
        task_3_2 = create_task(**{
            'project': project_3,
            'task_name': 'Task name' + postfix,
            'description': 'description',
            'start_date': start_date,
            'complete_date': complete_date,
            'author': employee,
            'assignee': employee,
            'status': NEW,
        })
        postfix = ' 4'
        task_1_1 = create_task(**{
            'project': project_1,
            'task_name': 'Task name' + postfix,
            'description': 'description',
            'start_date': start_date,
            'complete_date': complete_date,
            'author': employee,
            'assignee': employee,
            'status': COMPLETED,
        })
        postfix = ' 5'
        task_2_2 = create_task(**{
            'project': project_2,
            'task_name': 'Task name' + postfix,
            'description': 'description',
            'start_date': start_date,
            'complete_date': complete_date,
            'author': employee,
            'assignee': employee,
            'status': COMPLETED,
        })
        postfix = ' 6'
        task_3_3 = create_task(**{
            'project': project_3,
            'task_name': 'Task name' + postfix,
            'description': 'description',
            'start_date': start_date,
            'complete_date': complete_date,
            'author': employee,
            'assignee': employee,
            'status': COMPLETED,
        })

        qs_target = [
            {
                'project_name': 'Project name 1',
                'deadline': deadline,
                'budget': 100000.0,
                'closed': True,
                'tasks_count': 1,
                'percentage_completed': 100.0
            },
            {
                'project_name': 'Project name 2',
                'deadline': deadline,
                'budget': 100000.0,
                'closed': False,
                'tasks_count': 2,
                'percentage_completed': 50.0
            },
            {
                'project_name': 'Project name 3',
                'deadline': deadline,
                'budget': 100000.0,
                'closed': False,
                'tasks_count': 3,
                'percentage_completed': 33.33333333333333
            },
        ]
        response = self.client.get(reverse('projects:list'))
        fields = list(response.context['project_list']._fields)
        fields.remove('id')
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context['project_list'].values(*fields).order_by('id'),
            qs_target,
            transform=lambda x: x
        )


class ProjectDetailViewTest(TestCase):
    """todo

    """

    def test_project_with_tasks(self):
        """todo

        """
        deadline = timezone.now() + datetime.timedelta(days=32)
        start_date = timezone.now()
        complete_date = timezone.now() + datetime.timedelta(days=8)

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
        project_1 = create_project(**{
            'project_name': 'Project name' + postfix,
            'description': 'Project description' + postfix,
            'budget': 100000,
            'deadline': deadline,
            'closed': True,
        })
        task_1_1 = create_task(**{
            'project': project_1,
            'task_name': 'Task name' + postfix,
            'description': 'description',
            'start_date': start_date,
            'complete_date': complete_date,
            'author': employee,
            'assignee': employee,
            'status': NEW,
        })
        postfix = ' 2'
        task_1_2 = create_task(**{
            'project': project_1,
            'task_name': 'Task name' + postfix,
            'description': 'description',
            'start_date': start_date,
            'complete_date': complete_date,
            'author': employee,
            'assignee': employee,
            'status': NEW,
        })
        postfix = ' 3'
        task_1_3 = create_task(**{
            'project': project_1,
            'task_name': 'Task name' + postfix,
            'description': 'description',
            'start_date': start_date,
            'complete_date': complete_date,
            'author': employee,
            'assignee': employee,
            'status': NEW,
        })

        response = self.client.get(reverse('projects:detail', args=(project_1.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context['task_list'].order_by('id'),
            ["<Task: Task name 1>", "<Task: Task name 2>", "<Task: Task name 3>"]
        )

    def test_project_percentage_completed_without_tasks(self):
        """todo

        """
        deadline = timezone.now() + datetime.timedelta(days=32)
        postfix = ' 1'
        project_1 = create_project(**{
            'project_name': 'Project name' + postfix,
            'description': 'Project description' + postfix,
            'budget': 100000,
            'deadline': deadline,
            'closed': True,
        })

        response = self.client.get(reverse('projects:detail', args=(project_1.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, _("No tasks are available."))
        self.assertQuerysetEqual(response.context['task_list'], [])
        self.assertEqual(response.context['project']['percentage_completed'], 0.0)

    def test_projects_percentage_completed_with_three_tasks(self):
        """todo

        """
        deadline = timezone.now() + datetime.timedelta(days=32)
        start_date = timezone.now()
        complete_date = timezone.now() + datetime.timedelta(days=8)

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
        project_1 = create_project(**{
            'project_name': 'Project name' + postfix,
            'description': 'Project description' + postfix,
            'budget': 100000,
            'deadline': deadline,
            'closed': True,
        })
        task_1_1 = create_task(**{
            'project': project_1,
            'task_name': 'Task name' + postfix,
            'description': 'description',
            'start_date': start_date,
            'complete_date': complete_date,
            'author': employee,
            'assignee': employee,
            'status': NEW,
        })
        postfix = ' 2'
        task_1_2 = create_task(**{
            'project': project_1,
            'task_name': 'Task name' + postfix,
            'description': 'description',
            'start_date': start_date,
            'complete_date': complete_date,
            'author': employee,
            'assignee': employee,
            'status': COMPLETED,
        })
        postfix = ' 3'
        task_1_3 = create_task(**{
            'project': project_1,
            'task_name': 'Task name' + postfix,
            'description': 'description',
            'start_date': start_date,
            'complete_date': complete_date,
            'author': employee,
            'assignee': employee,
            'status': COMPLETED,
        })
        postfix = ' 4'
        task_1_4 = create_task(**{
            'project': project_1,
            'task_name': 'Task name' + postfix,
            'description': 'description',
            'start_date': start_date,
            'complete_date': complete_date,
            'author': employee,
            'assignee': employee,
            'status': COMPLETED,
        })

        response = self.client.get(reverse('projects:detail', args=(project_1.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context['task_list'].order_by('id'),
            ["<Task: Task name 1>", "<Task: Task name 2>",
             "<Task: Task name 3>", "<Task: Task name 4>"]
        )
        self.assertEqual(response.context['project']['percentage_completed'], 75.0)


class ProjectCreateViewTest(TestCase):
    """todo

    """



class TaskModelTest(TestCase):
    """todo

    """

    def test_model_str(self):
        """todo

        """
        deadline = timezone.now() + datetime.timedelta(days=32)
        start_date = timezone.now()
        complete_date = timezone.now() + datetime.timedelta(days=8)

        postfix = ' 1'
        project_1 = create_project(**{
            'project_name': 'Project name' + postfix,
            'description': 'Project description' + postfix,
            'budget': 100000,
            'deadline': deadline,
            'closed': True,
        })
        task_1_1_str = create_task(**{
            'project': project_1,
            'task_name': 'Task name' + postfix,
            'description': 'description',
            'start_date': start_date,
            'complete_date': complete_date,
            'author': None,
            'assignee': None,
            'status': NEW,
        }).__str__()
        task_str_target = 'Task name 1'
        self.assertEqual(task_1_1_str, task_str_target)

    def test_get_status_repr(self):
        """todo

        """
        deadline = timezone.now() + datetime.timedelta(days=32)
        start_date = timezone.now()
        complete_date = timezone.now() + datetime.timedelta(days=8)

        postfix = ' 1'
        project_1 = create_project(**{
            'project_name': 'Project name' + postfix,
            'description': 'Project description' + postfix,
            'budget': 100000,
            'deadline': deadline,
            'closed': True,
        })
        task_1_1 = create_task(**{
            'project': project_1,
            'task_name': 'Task name' + postfix,
            'description': 'description',
            'start_date': start_date,
            'complete_date': complete_date,
            'author': None,
            'assignee': None,
            'status': NEW,
        })
        status_new = task_1_1.get_status_repr()
        task_1_1.status = IN_PROGRESS
        status_in_progress = task_1_1.get_status_repr()
        task_1_1.status = COMPLETED
        status_completed = task_1_1.get_status_repr()
        status_new_target = _('New')
        status_in_progress_target = _('In progress')
        status_completed_target = _('Finished')
        self.assertEqual(status_new, status_new_target)
        self.assertEqual(status_in_progress, status_in_progress_target)
        self.assertEqual(status_completed, status_completed_target)


class TaskListViewTest(TestCase):
    """todo

    """

    def test_no_tasks(self):
        """todo

        """
        response = self.client.get(reverse('projects:task_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, _("No tasks are available."))
        self.assertQuerysetEqual(response.context['task_list'], [])

    def test_two_tasks(self):
        """todo

        """
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

        deadline = timezone.now() + datetime.timedelta(days=32)
        start_date = timezone.now()
        complete_date = timezone.now() + datetime.timedelta(days=8)

        postfix = ' 1'
        project_1 = create_project(**{
            'project_name': 'Project name' + postfix,
            'description': 'Project description' + postfix,
            'budget': 100000,
            'deadline': deadline,
            'closed': True,
        })
        task_1_1 = create_task(**{
            'project': project_1,
            'task_name': 'Task name' + postfix,
            'description': 'description',
            'start_date': start_date,
            'complete_date': complete_date,
            'author': employee,
            'assignee': employee,
            'status': NEW,
        })
        postfix = ' 2'
        task_1_2 = create_task(**{
            'project': project_1,
            'task_name': 'Task name' + postfix,
            'description': 'description',
            'start_date': start_date,
            'complete_date': complete_date,
            'author': employee,
            'assignee': employee,
            'status': NEW,
        })
        response = self.client.get(reverse('projects:task_list'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context['task_list'].order_by('id'),
            ['<Task: Task name 1>', '<Task: Task name 2>']
        )


class TaskDetailViewTest(TestCase):
    """todo

    """

    def test_task_without_comments(self):
        """todo

        """
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

        deadline = timezone.now() + datetime.timedelta(days=32)
        start_date = timezone.now()
        complete_date = timezone.now() + datetime.timedelta(days=8)

        postfix = ' 1'
        project_1 = create_project(**{
            'project_name': 'Project name' + postfix,
            'description': 'Project description' + postfix,
            'budget': 100000,
            'deadline': deadline,
            'closed': True,
        })
        task_1_1 = create_task(**{
            'project': project_1,
            'task_name': 'Task name' + postfix,
            'description': 'description',
            'start_date': start_date,
            'complete_date': complete_date,
            'author': employee,
            'assignee': employee,
            'status': NEW,
        })
        response = self.client.get(reverse('projects:task_detail', args=(task_1_1.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, _("No comments are available."))
        self.assertQuerysetEqual(task_1_1.comments.all(), [])

    def test_task_with_comments(self):
        """todo

        """
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

        deadline = timezone.now() + datetime.timedelta(days=32)
        start_date = timezone.now()
        complete_date = timezone.now() + datetime.timedelta(days=8)

        postfix = ' 1'
        project_1 = create_project(**{
            'project_name': 'Project name' + postfix,
            'description': 'Project description' + postfix,
            'budget': 100000,
            'deadline': deadline,
            'closed': True,
        })
        task_1_1 = create_task(**{
            'project': project_1,
            'task_name': 'Task name' + postfix,
            'description': 'description',
            'start_date': start_date,
            'complete_date': complete_date,
            'author': employee,
            'assignee': employee,
            'status': NEW,
        })
        Comment.objects.create(**{'task': task_1_1, 'text': 'comment 1'})
        Comment.objects.create(**{'task': task_1_1, 'text': 'comment 2'})
        Comment.objects.create(**{'task': task_1_1, 'text': 'comment 3'})
        response = self.client.get(reverse('projects:task_detail', args=(task_1_1.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            task_1_1.comments.all().order_by('id'),
            ['<Comment: comment 1>', '<Comment: comment 2>', '<Comment: comment 3>']
        )
