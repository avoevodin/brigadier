from django.test import TestCase
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model, authenticate, get_user
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import AnonymousUser

from .admin import UserCreationForm

User = get_user_model()


class AccountRegistrationViewTest(TestCase):
    """Tests for registration view.

    """

    def test_create_user_public_group_exists(self):
        """Test checks home page availability with public.

        """
        group_public = Group.objects.get(name='public')
        response = self.client.post(
            reverse('accounts:registration'),
            {
                'username': 'User_name',
                'email': 'user@example.com',
                'password1': '1234',
                'password2': '1234',
            }
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('accounts:registration_done'))

        user = User.objects.first()
        self.assertQuerysetEqual(user.groups.all(), [group_public], transform=lambda x: x)

    def test_create_user_public_group_does_not_exists(self):
        """Test check that home page isn't available if the
        public group doesn't exist in user's account.

        """
        group_public = Group.objects.get(name='public')
        group_public.delete()
        response = self.client.post(
            reverse('accounts:registration'),
            {
                'username': 'User_name',
                'email': 'user@example.com',
                'password1': '1234',
                'password2': '1234',
            }
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('accounts:registration_done'))

        user = User.objects.first()
        self.assertQuerysetEqual(user.groups.all(), [], transform=lambda x: x)


class UserCreationTest(TestCase):
    """todo

    """

    def test_create_user_admin_different_passwords(self):
        """todo

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
        """todo

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
        """todo

        """
        username = 'test'
        email = 'test@example.com'
        password = '1234'
        form = UserCreationForm(
            {'email': email, 'username': username, 'password1': password,
            'password2':password}
        )
        user = form.save()
        self.assertEqual(user, get_object_or_404(User, email=email))


class AuthenticationTest(TestCase):
    """todo

    """
    def test_authenticate_not_existed_user(self):
        """todo

        """
        user = authenticate(username='test', password='1234')
        self.assertEqual(user, None)

    def test_authenticate_user(self):
        """todo

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
        """todo

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
        """todo

        """
        user = authenticate(email='test@example.com', password='1234')
        self.assertEqual(user, None)

    def test_authenticate_user_with_email(self):
        """todo

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
        """todo

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
