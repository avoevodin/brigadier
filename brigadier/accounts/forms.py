from django import forms
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField
from django.contrib.auth.models import User


class AccountRegistrationForm(UserCreationForm):
    """todo

    """
    username = UsernameField(
        widget=forms.TextInput(attrs={
            'autofocus': True,
            'class': 'form-control mb-2',
            'placeholder': _('Username'),
        })
    )
    password1 = forms.CharField(
        label=_('Enter password'),
        widget=forms.PasswordInput(attrs={
            'class': 'form-control mb-2',
            'required': 'true',
            'placeholder': _('Enter password'),
        })
    )
    password2 = forms.CharField(
        label=_('Confirm password'),
        widget=forms.PasswordInput(attrs={
            'class': 'form-control mb-2',
            'required': 'true',
            'placeholder': _('Confirm password'),
        }),
    )

    class Meta:
        model = User
        fields = ['username']


class AccountLoginForm(AuthenticationForm):
    """todo

    """
    username = UsernameField(
        widget=forms.TextInput(attrs={
            'autofocus': True,
            'class': 'form-control mb-2',
            'placeholder': _('Username'),
        })
    )
    password = forms.CharField(
        label=_('Enter password'),
        widget=forms.PasswordInput(attrs={
            'class': 'form-control mb-2',
            'required': 'true',
            'placeholder': _('Enter password'),
        })
    )

    class Meta:
        model = User
        fields = ['username']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control mb-2',
                'placeholder': _('Username'),
            }),
        }
