from django import forms
from django.contrib.auth import password_validation, get_user_model
from django.contrib.auth.forms import (UserCreationForm, AuthenticationForm,
                                       UsernameField, PasswordChangeForm)
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class AccountRegistrationForm(UserCreationForm):
    """Registration form.

    """
    username = UsernameField(
        widget=forms.TextInput(attrs={
            'autofocus': True,
            'class': 'form-control mb-2',
            'placeholder': _('Username'),
        })
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'autofocus': True,
            'class': 'form-control mb-2',
            'placeholder': _('Email'),
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
        fields = ['username', 'email']


class AccountLoginForm(AuthenticationForm):
    """Authentication form.

    """
    username = UsernameField(
        widget=forms.TextInput(attrs={
            'autofocus': True,
            'class': 'form-control mb-2',
            'placeholder': _('Email or username'),
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
    """Change password form.

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
