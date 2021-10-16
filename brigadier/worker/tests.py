import datetime
import os
from unittest import mock
from unittest.mock import call
from uuid import uuid4

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core import mail
from django.test import TestCase
from django.utils import timezone
from employees.tests import create_employee
from projects.models import NEW, IN_PROGRESS
from projects.tests import create_project, create_task

from .email.tasks import send_verification_mail, send_onboarding_mail, \
    get_overdue_emails, create_overdue_notification_tasks, \
    send_overdue_notification_email

User = get_user_model()


class WorkerEmailTest(TestCase):
    """Tests for celery worker email tasks.

    """

    def test_send_verification_mail(self):
        """Test sending verification email.

        """
        email = 'test@example.com'

        key = uuid4().hex
        confirm = uuid4().hex
        host = 'testserver'
        send_verification_mail(host, email, key, confirm)
        self.assertEqual(len(mail.outbox), 1)
        activation_mail = mail.outbox[0]
        self.assertEqual(activation_mail.subject, 'Activate your account.')
        self.assertEqual(activation_mail.from_email, settings.DEFAULT_FROM_EMAIL)
        self.assertEqual(activation_mail.to, [email])
        mail.outbox = []

    def test_send_onboarding_mail(self):
        """Test for sending onboarding email.

        """
        email = 'test@example.com'
        host = 'testserver'
        send_onboarding_mail(host, email)
        self.assertEqual(len(mail.outbox), 1)
        activation_mail = mail.outbox[0]
        self.assertEqual(activation_mail.subject, 'Welcome!')
        self.assertEqual(activation_mail.from_email, settings.DEFAULT_FROM_EMAIL)
        self.assertEqual(activation_mail.to, [email])
        mail.outbox = []

    def test_get_overdue_emails_without_overdue_tasks(self):
        """Test for getting overdue emails without overdue tasks.

        """
        postfix = ' 1'
        username = 'test'
        email = 'user@example.com'
        password = 'test'
        usr = User.objects.create_user(username=username, password=password, email=email, )

        deadline = timezone.now() + datetime.timedelta(days=32)
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
            'user': usr,
            'birthdate': birthdate,
        })
        project = create_project(**{
            'project_name': 'Project name' + postfix,
            'description': 'Project description' + postfix,
            'budget': 100000,
            'deadline': deadline,
            'closed': True,
        })
        create_task(**{
            'project': project,
            'task_name': 'Task name' + postfix,
            'description': 'description',
            'start_date': start_date,
            'complete_date': complete_date,
            'author': employee,
            'assignee': employee,
            'status': NEW,
        })

        overdue_emails = get_overdue_emails()
        self.assertQuerysetEqual(overdue_emails, [])

    def test_get_overdue_tasks_with_overdue_tasks(self):
        """Test for getting overdue emails with some overdue tasks.

        """
        postfix = ' 1'
        username = 'test'
        email = 'user@example.com'
        password = 'test'
        usr = User.objects.create_user(username=username, password=password, email=email, )

        deadline = timezone.now() + datetime.timedelta(days=32)
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
            'user': usr,
            'birthdate': birthdate,
        })
        project = create_project(**{
            'project_name': 'Project name' + postfix,
            'description': 'Project description' + postfix,
            'budget': 100000,
            'deadline': deadline,
            'closed': True,
        })
        create_task(**{
            'project': project,
            'task_name': 'Task name' + postfix,
            'description': 'description',
            'start_date': start_date,
            'complete_date': complete_date,
            'author': employee,
            'assignee': employee,
            'status': NEW,
        })
        postfix = '2'
        start_date = timezone.now() - datetime.timedelta(days=9)
        complete_date = timezone.now() - datetime.timedelta(days=8)
        create_task(**{
            'project': project,
            'task_name': 'Task name' + postfix,
            'description': 'description',
            'start_date': start_date,
            'complete_date': complete_date,
            'author': employee,
            'assignee': employee,
            'status': IN_PROGRESS,
        })
        postfix = '3'
        start_date = timezone.now() - datetime.timedelta(days=8)
        complete_date = timezone.now() - datetime.timedelta(minutes=64)
        create_task(**{
            'project': project,
            'task_name': 'Task name' + postfix,
            'description': 'description',
            'start_date': start_date,
            'complete_date': complete_date,
            'author': employee,
            'assignee': employee,
            'status': NEW,
        })
        postfix = '4'
        start_date = timezone.now() - datetime.timedelta(days=8)
        complete_date = timezone.now() - datetime.timedelta(minutes=64)
        create_task(**{
            'project': project,
            'task_name': 'Task name' + postfix,
            'description': 'description',
            'start_date': start_date,
            'complete_date': complete_date,
            'author': employee,
            'assignee': employee,
            'status': IN_PROGRESS,
        })

        overdue_emails = get_overdue_emails()
        self.assertQuerysetEqual(
            overdue_emails,
            [{
                'email': 'user@example.com',
                'tasks_list_str':
                    'Task "Task name2" overdue for 8 days and 0 hours.\n'
                    'Task "Task name4" overdue for 0 days and 1 hours.\n'}]
        )

    def test_create_overdue_notification_tasks(self):
        """Test for creating overdue notification tasks.

        """
        postfix = ' 1'
        username = 'test'
        email = 'user@example.com'
        password = 'test'
        usr = User.objects.create_user(username=username, password=password, email=email, )

        deadline = timezone.now() + datetime.timedelta(days=32)
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
            'user': usr,
            'birthdate': birthdate,
        })
        project = create_project(**{
            'project_name': 'Project name' + postfix,
            'description': 'Project description' + postfix,
            'budget': 100000,
            'deadline': deadline,
            'closed': True,
        })
        create_task(**{
            'project': project,
            'task_name': 'Task name' + postfix,
            'description': 'description',
            'start_date': start_date,
            'complete_date': complete_date,
            'author': employee,
            'assignee': employee,
            'status': NEW,
        })
        postfix = '2'
        start_date = timezone.now() - datetime.timedelta(days=9)
        complete_date = timezone.now() - datetime.timedelta(days=8)
        create_task(**{
            'project': project,
            'task_name': 'Task name' + postfix,
            'description': 'description',
            'start_date': start_date,
            'complete_date': complete_date,
            'author': employee,
            'assignee': employee,
            'status': IN_PROGRESS,
        })
        postfix = '3'
        start_date = timezone.now() - datetime.timedelta(days=8)
        complete_date = timezone.now() - datetime.timedelta(minutes=64)
        create_task(**{
            'project': project,
            'task_name': 'Task name' + postfix,
            'description': 'description',
            'start_date': start_date,
            'complete_date': complete_date,
            'author': employee,
            'assignee': employee,
            'status': NEW,
        })
        postfix = '4'
        start_date = timezone.now() - datetime.timedelta(days=8)
        complete_date = timezone.now() - datetime.timedelta(minutes=64)
        create_task(**{
            'project': project,
            'task_name': 'Task name' + postfix,
            'description': 'description',
            'start_date': start_date,
            'complete_date': complete_date,
            'author': employee,
            'assignee': employee,
            'status': IN_PROGRESS,
        })

        with mock.patch('worker.email.tasks.send_overdue_notification_email.delay') as m:
            create_overdue_notification_tasks()
        m.assert_called_once_with(
            'user@example.com',
            'Task "Task name2" overdue for 8 days and 0 hours.\n'
            'Task "Task name4" overdue for 0 days and 1 hours.\n'
        )

    def test_create_overdue_notification_tasks_several_users(self):
        """Test for creating overdue notification tasks. Several users has
        overdue tasks.

        """
        postfix = ' 1'
        username = 'test 1'
        email = 'user1@example.com'
        password = 'test'
        usr1 = User.objects.create_user(username=username, password=password, email=email, )

        username = 'test 2'
        email = 'user2@example.com'
        password = 'test'
        usr2 = User.objects.create_user(username=username, password=password, email=email, )

        deadline = timezone.now() + datetime.timedelta(days=32)
        start_date = timezone.now()
        complete_date = timezone.now() + datetime.timedelta(days=8)

        firstname = 'Marshall ' + postfix
        middlename = 'Bruce ' + postfix
        surname = 'Mathers ' + postfix
        email = f'mbm{postfix}@example.com'
        birthdate = timezone.now() + datetime.timedelta(days=-365 * 30)

        employee1 = create_employee(**{
            'firstname': firstname,
            'middlename': middlename,
            'surname': surname,
            'email': email,
            'user': usr1,
            'birthdate': birthdate,
        })

        postfix = '2'
        firstname = 'Marshall ' + postfix
        middlename = 'Bruce ' + postfix
        surname = 'Mathers ' + postfix
        email = f'mbm{postfix}@example.com'
        birthdate = timezone.now() + datetime.timedelta(days=-365 * 30)

        employee2 = create_employee(**{
            'firstname': firstname,
            'middlename': middlename,
            'surname': surname,
            'email': email,
            'user': usr2,
            'birthdate': birthdate,
        })

        postfix = ' 1'
        project = create_project(**{
            'project_name': 'Project name' + postfix,
            'description': 'Project description' + postfix,
            'budget': 100000,
            'deadline': deadline,
            'closed': True,
        })
        create_task(**{
            'project': project,
            'task_name': 'Task name' + postfix,
            'description': 'description',
            'start_date': start_date,
            'complete_date': complete_date,
            'author': employee1,
            'assignee': employee1,
            'status': NEW,
        })
        postfix = '2'
        start_date = timezone.now() - datetime.timedelta(days=9)
        complete_date = timezone.now() - datetime.timedelta(days=8)
        create_task(**{
            'project': project,
            'task_name': 'Task name' + postfix,
            'description': 'description',
            'start_date': start_date,
            'complete_date': complete_date,
            'author': employee1,
            'assignee': employee1,
            'status': IN_PROGRESS,
        })
        postfix = '3'
        start_date = timezone.now() - datetime.timedelta(days=8)
        complete_date = timezone.now() - datetime.timedelta(minutes=64)
        create_task(**{
            'project': project,
            'task_name': 'Task name' + postfix,
            'description': 'description',
            'start_date': start_date,
            'complete_date': complete_date,
            'author': employee2,
            'assignee': employee2,
            'status': NEW,
        })
        postfix = '4'
        start_date = timezone.now() - datetime.timedelta(days=8)
        complete_date = timezone.now() - datetime.timedelta(minutes=64)
        create_task(**{
            'project': project,
            'task_name': 'Task name' + postfix,
            'description': 'description',
            'start_date': start_date,
            'complete_date': complete_date,
            'author': employee2,
            'assignee': employee2,
            'status': IN_PROGRESS,
        })

        with mock.patch('worker.email.tasks.send_overdue_notification_email.delay') as m:
            create_overdue_notification_tasks()
        m.assert_has_calls(
            [
                call('user1@example.com',
                     'Task "Task name2" overdue for 8 days and 0 hours.\n'),
                call('user2@example.com',
                     'Task "Task name4" overdue for 0 days and 1 hours.\n'),
            ],
            True
        )

    def test_send_overdue_notification_email(self):
        """Test for sending overdue notification mail.

        """
        email = 'user@example.com'
        overdue_tasks = \
            'Task "Task name2" overdue for 8 days and 0 hours.\n' \
            'Task "Task name4" overdue for 0 days and 1 hours.\n'
        send_overdue_notification_email(
            email,
            overdue_tasks
        )
        self.assertEqual(len(mail.outbox), 1)
        overdue_mail = mail.outbox[0]
        self.assertEqual(overdue_mail.subject, 'Hello!')
        self.assertEqual(overdue_mail.from_email, settings.DEFAULT_FROM_EMAIL)
        self.assertEqual(overdue_mail.to, [email])
        self.assertEqual(
            overdue_mail.body,
            'Seems that you have some overdue tasks here:\n'
            + overdue_tasks
        )
        mail.outbox = []


class WorkerAppTest(TestCase):
    """Testing configs with different env vars

    """

    def test_broker_url_with_rabbit_envs(self):
        """Testing celery config with set rabbitMQ env vars.

        """
        with mock.patch.dict(os.environ, {
            'RABBITMQ_HOST': '0.0.0.0',
            'RABBITMQ_PORT': '8888',
            'RABBITMQ_DEFAULT_USER': 'test',
            'RABBITMQ_DEFAULT_PASS': 'password',
            'RABBITMQ_DEFAULT_VHOST': 'celery_test',
        }):
            import importlib
            from worker import app

            importlib.reload(app)
            self.assertEqual(app.broker_url, 'pyamqp://test:password@0.0.0.0:8888/celery_test')

    def test_broker_url_without_rabbit_envs(self):
        """Testing celery config with set rabbitMQ env vars.

        """
        with mock.patch.dict(os.environ, {
            'RABBITMQ_HOST': '',
            'RABBITMQ_PORT': '',
            'RABBITMQ_DEFAULT_USER': '',
            'RABBITMQ_DEFAULT_PASS': '',
            'RABBITMQ_DEFAULT_VHOST': '',
        }):
            import importlib
            from worker import app

            importlib.reload(app)
            self.assertIsNone(app.broker_url, None)
