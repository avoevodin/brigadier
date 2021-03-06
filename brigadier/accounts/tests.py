from django.test import TestCase
from django.contrib.auth.models import Group, User
from django.urls import reverse


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
                'password1': '1234',
                'password2': '1234',
            }
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('accounts:registration_done'))

        user = User.objects.first()
        self.assertQuerysetEqual(user.groups.all(), [], transform=lambda x: x)
