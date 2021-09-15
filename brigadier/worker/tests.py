from uuid import uuid4

from django.test import TestCase
from .email.tasks import send_verification_mail
from django.conf import settings
from django.core import mail


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
