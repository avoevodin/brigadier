from uuid import uuid4

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core import mail
from django.core.cache import cache
from django.test import TestCase

from .email.tasks import send_verification_mail

User = get_user_model()


class WorkerEmailTest(TestCase):
    """todo

    """

    def test_send_verification_mail(self):
        """todo

        """
        username = 'test'
        password = 'test'
        email = 'test@example.com'

        user = User.objects.create_user(
            username=username, password=password, email=email,
            commit=False, is_active=False
        )
        user.save()

        key = uuid4().hex
        confirm = uuid4().hex
        data = {
            'confirm': confirm,
            'user_id': user.id,
        }
        cache.set(key, data, settings.EXPIRE_LINK)
        host = 'testserver'
        send_verification_mail(host, email, key, confirm)
        self.assertEqual(len(mail.outbox), 1)
        activation_mail = mail.outbox[0]
        self.assertEqual(activation_mail.subject, 'Activate your email.')
        self.assertEqual(activation_mail.from_email, settings.DEFAULT_FROM_EMAIL)
        self.assertEqual(activation_mail.to, [email])
