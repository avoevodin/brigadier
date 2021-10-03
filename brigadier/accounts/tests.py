import re
from unittest import mock
from unittest.mock import ANY

from django.conf import settings
from django.contrib.auth import get_user_model, authenticate, get_user
from django.contrib.auth.models import AnonymousUser
from django.contrib.sites.shortcuts import get_current_site
from django.core import mail
from django.core.cache import cache
from django.shortcuts import get_object_or_404
from django.test import TestCase
from django.urls import reverse
from django.utils.translation import gettext as _

from .admin import UserCreationForm

User = get_user_model()


class AccountRegistrationViewTest(TestCase):
    """Tests for registration view.

    """

    # def test_create_user_public_group_exists(self):
    #     """Test checks home page availability with public.
    #
    #     """
    #     group_public = Group.objects.get(name='public')
    #     response = self.client.post(
    #         reverse('accounts:registration'),
    #         {
    #             'username': 'User_name',
    #             'email': 'user@example.com',
    #             'password1': '1234',
    #             'password2': '1234',
    #         }
    #     )
    #     self.assertEqual(response.status_code, 302)
    #     self.assertEqual(response.url, reverse('accounts:registration_done'))
    #
    #     user = User.objects.first()
    #     self.assertQuerysetEqual(user.groups.all(), [group_public], transform=lambda x: x)
    #
    # def test_create_user_public_group_does_not_exists(self):
    #     """Test check that home page isn't available if the
    #     public group doesn't exist in user's account.
    #
    #     """
    #     group_public = Group.objects.get(name='public')
    #     group_public.delete()
    #     response = self.client.post(
    #         reverse('accounts:registration'),
    #         {
    #             'username': 'User_name',
    #             'email': 'user@example.com',
    #             'password1': '1234',
    #             'password2': '1234',
    #         }
    #     )
    #     self.assertEqual(response.status_code, 302)
    #     self.assertEqual(response.url, reverse('accounts:registration_done'))
    #
    #     user = User.objects.first()
    #     self.assertQuerysetEqual(user.groups.all(), [], transform=lambda x: x)
    #

class AccountRegistrationActivateViewTest(TestCase):
    """Tests for account registration activate by the link
    passed to user's email.

    """

    # def test_account_activate_from_email_with_error(self):
    #     """Activate an account with wrong activation link.
    #
    #     """
    #     username = 'test'
    #     email = 'test@example.com'
    #     password = '1234'
    #     response = self.client.post(
    #         reverse('accounts:registration'),
    #         {
    #             'username': username,
    #             'email': email,
    #             'password1': password,
    #             'password2': password,
    #         }
    #     )
    #     self.assertEqual(response.status_code, 302)
    #     self.assertEqual(response.url, reverse('accounts:registration_done'))
    #
    #     user = get_object_or_404(User, email=email)
    #     self.assertEqual(user.is_active, False)
    #     self.assertEqual(len(mail.outbox), 1)
    #     activate_mail = mail.outbox[0]
    #     self.assertEqual(activate_mail.subject, 'Activate your email.')
    #     self.assertEqual(activate_mail.from_email, settings.DEFAULT_FROM_EMAIL)
    #     self.assertEqual(activate_mail.to, [user.email])
    #     host = 'http://testserver'
    #     activation_path = reverse(
    #         "accounts:registration_activate",
    #         args=(
    #             'wrong_key', 'wrong_confirm',
    #         )
    #     )
    #     activation_url = f'{host}{activation_path}'
    #     response = self.client.get(activation_url)
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(response.context_data['message'], 'error')
    #     user.refresh_from_db()
    #     self.assertEqual(user.is_active, False)

    def test_account_activate_from_email(self):
        """Activate an account with correct activation link.

        """
        username = 'test'
        email = 'test@example.com'
        password = '1234'
        with mock.patch('worker.email.tasks.send_verification_mail.delay') as m:
            response = self.client.post(
                reverse('accounts:registration'),
                {
                    'username': username,
                    'email': email,
                    'password1': password,
                    'password2': password,
                }
            )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('accounts:registration_done'))
        host = get_current_site(response.wsgi_request).domain
        m.assert_called_once_with(host, email, ANY, ANY)
        call_args = m.call_args.args
        key = call_args[2]
        confirm = call_args[3]
        user = get_object_or_404(User, email=email)
        self.assertEqual(user.is_active, False)
        # self.assertEqual(len(mail.outbox), 1)
        # activation_mail = mail.outbox[0]
        # self.assertEqual(activation_mail.subject, 'Activate your email.')
        # self.assertEqual(activation_mail.from_email, settings.DEFAULT_FROM_EMAIL)
        # self.assertEqual(activation_mail.to, [user.email])
        activation_url = 'http://' + host \
            + reverse("accounts:registration_activate", args=(key, confirm))
        # activation_url = re.search("(?P<url>http?://[^\s]+)",
        #                            activation_mail.body).group("url")
        response = self.client.get(activation_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context_data['message'], 'ok')
        user.refresh_from_db()
        self.assertEqual(user.is_active, True)


class UserCreationTest(TestCase):
    """Custom user model creation tests.

    """

    def test_create_user_admin_different_passwords(self):
        """Create user with not matching passwords.

        """
        username = 'admin'
        email = 'admin@example.com'
        password = '1234'
        User.objects.create_user(
            username=username, password=password, email=email,
            is_admin=True, is_superuser=True,
        )
        self.client.login(username=username, password=password)
        response = self.client.post(
            reverse('admin:accounts_myuser_add'),
            data={
                'username': 'test',
                'email': 'test@example.com',
                'password1': '1234',
                'password2': '12345',
            }
        )
        self.assertEqual(response.context_data['errors'].data, [["Passwords don't match"]])

    def test_create_user_admin(self):
        """Test opening user change form through
        the admin panel.

        """
        username = 'admin'
        email = 'admin@example.com'
        password = '1234'
        User.objects.create_user(
            username=username, password=password, email=email,
            is_admin=True, is_superuser=True,
        )
        self.client.login(username=username, password=password)

        username = 'test'
        email = 'test@example.com'
        password = '1234'
        response = self.client.post(
            reverse('admin:accounts_myuser_add'),
            data={
                'username': username,
                'email': email,
                'password1': password,
                'password2': password,
            }
        )
        usr = get_object_or_404(User, email=email)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('admin:accounts_myuser_change', args=(usr.id,)))

    def test_create_user_form_save(self):
        """Test saving user creation form through
        the admin panel.

        """
        username = 'test'
        email = 'test@example.com'
        password = '1234'
        form = UserCreationForm(
            {'email': email, 'username': username, 'password1': password,
             'password2': password}
        )
        user = form.save()
        self.assertEqual(user, get_object_or_404(User, email=email))


class AuthenticationTest(TestCase):
    """Test custom user model authentication.

    """

    def test_authenticate_not_existed_user(self):
        """Authenticate not existed user.

        """
        user = authenticate(username='test', password='1234')
        self.assertEqual(user, None)

    def test_authenticate_user(self):
        """Authenticate existed user.

        """
        username = 'test'
        email = 'test@example.com'
        password = '1234'
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        auth_user = authenticate(username=username, password=password)
        self.assertEqual(user, auth_user)
        self.client.login(username=username, password=password)
        session_user = get_user(self.client)
        self.assertEqual(auth_user, session_user)

    def test_authenticate_user_with_its_deletion_after_login(self):
        """Get authenticated user after deleting this user.

        """
        username = 'test'
        email = 'test@example.com'
        password = '1234'
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        auth_user = authenticate(username=username, password=password)
        self.assertEqual(user, auth_user)
        self.client.login(username=username, password=password)
        auth_user.delete()
        session_user = get_user(self.client)
        self.assertEqual(AnonymousUser(), session_user)

    def test_authenticate_not_existed_user_with_email(self):
        """Authenticate not existed user with email.

        """
        user = authenticate(email='test@example.com', password='1234')
        self.assertEqual(user, None)

    def test_authenticate_user_with_email(self):
        """Authenticate existed user with email.

        """
        username = 'test'
        email = 'test@example.com'
        password = '1234'
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        auth_user = authenticate(username=email, password=password)
        self.assertEqual(user, auth_user)

    def test_authenticate_user_wrong_password(self):
        """Authenticate user with wrong password.

        """
        username = 'test'
        email = 'test@example.com'
        password = '1234'
        User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        auth_user = authenticate(username=username, password='mistake')
        self.assertEqual(auth_user, None)


class MyUserManagerModelTest(TestCase):
    """Tests for manager of custom User model MyUser.

    """

    def test_create_user_without_email(self):
        """Create user without email.

        """
        username = 'test'
        password = '1234'
        with self.assertRaises(
                ValueError,
                msg=_('Users must have a username and an email address')
        ):
            User.objects.create_user(
                username=username,
                password=password,
            )

    def test_create_superuser(self):
        """Create superuser.

        """
        username = 'admin'
        email = 'admin@example.com'
        password = '1234'
        superuser = User.objects.create_superuser(
            username=username,
            email=email,
            password=password,
        )
        self.assertEqual(superuser.is_admin, True)
        self.assertEqual(superuser.is_superuser, True)

    def test_create_superuser_is_not_admin(self):
        """Create superuser with is_admin=False.

        """
        username = 'admin'
        email = 'admin@example.com'
        password = '1234'
        with self.assertRaises(
                ValueError,
                msg=_('Superuser must have is_admin=True.')
        ):
            User.objects.create_superuser(
                username=username,
                email=email,
                password=password,
                is_admin=False
            )

    def test_create_superuser_is_not_superuser(self):
        """Create superuser with is_superuser=False.

        """
        username = 'admin'
        email = 'admin@example.com'
        password = '1234'
        with self.assertRaises(
                ValueError,
                msg=_('Superuser must have is_superuser=True.')
        ):
            User.objects.create_superuser(
                username=username,
                email=email,
                password=password,
                is_superuser=False
            )


class MyUserModelTest(TestCase):
    """Tests for custom User model MyUser.

    """

    def test_full_name(self):
        """Get full name of the user.

        """
        username = 'test'
        email = 'test@example.com'
        password = '1234'
        first_name = ' Mike'
        last_name = 'Johnson '
        usr = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )
        self.assertEqual(usr.get_full_name(), 'Mike Johnson')

    def test_email_user(self):
        """Email to user.

        """
        username = 'test'
        email = 'test@example.com'
        password = '1234'
        first_name = ' Mike'
        last_name = 'Johnson '
        usr = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )
        subject = 'Test subject'
        message = f'Hello, dear {usr.get_full_name()}!'
        usr.email_user(subject, message)
        self.assertEqual(len(mail.outbox), 1)
        sent_mail = mail.outbox[0]
        self.assertEqual(sent_mail.subject, subject)
        self.assertEqual(sent_mail.body, message)
        self.assertEqual(sent_mail.from_email, settings.DEFAULT_FROM_EMAIL)
        self.assertEqual(sent_mail.to, [usr.email])
