from django import forms
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import (UserCreationForm, AuthenticationForm,
                                       UsernameField, PasswordChangeForm)
from django.contrib.auth.models import User
from django.contrib.auth import password_validation


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
        strip=False,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control mb-2',
            'required': 'true',
            'placeholder': _('Enter password'),
        })
    )
    password2 = forms.CharField(
        strip=False,
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
        strip=False,
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


class AccountPasswordChangeForm(PasswordChangeForm):
    """todo

    """
    old_password = forms.CharField(
        strip=False,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control mb-2',
            'required': 'true',
            'placeholder': _('Old password'),
            'autocomplete': 'current-password',
            'autofocus': True
        }),
    )
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control mb-2',
            'required': 'true',
            'placeholder': _('New password'),
            'autocomplete': 'new-password',
        }),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        strip=False,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control mb-2',
            'required': 'true',
            'placeholder': _('Confirm password'),
            'autocomplete': 'new-password',
        }),
    )
