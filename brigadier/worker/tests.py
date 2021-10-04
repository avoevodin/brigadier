import os
from uuid import uuid4

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core import mail
from unittest import TestCase, mock
from .email.tasks import send_verification_mail, send_onboarding_mail

User = get_user_model()


class WorkerEmailTest(TestCase):
    """todo

    """

    def test_send_verification_mail(self):
        """todo

        """
        email = 'test@example.com'

        key = uuid4().hex
        confirm = uuid4().hex
        host = 'testserver'
        send_verification_mail(host, email, key, confirm)
        self.assertEqual(len(mail.outbox), 1)
        activation_mail = mail.outbox[0]
        self.assertEqual(activation_mail.subject, 'Activate your email.')
        self.assertEqual(activation_mail.from_email, settings.DEFAULT_FROM_EMAIL)
        self.assertEqual(activation_mail.to, [email])
        mail.outbox = []

    def test_send_onboarding_mail(self):
        """todo

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
