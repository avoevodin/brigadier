from django import forms
from django.contrib.auth import password_validation, get_user_model
from django.contrib.auth.forms import (UserCreationForm, AuthenticationForm,
                                       UsernameField, PasswordChangeForm)
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from django.forms import ModelForm, CharField, PasswordInput
from .models import MyUser

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

class UserCreationForm(ModelForm):
    """Custom user creation form

    """
    password1 = CharField(label=_('Password'), widget=PasswordInput)
    password2 = CharField(label=_('Confirm password'), widget=PasswordInput)

    class Meta:
        model = MyUser
        fields = ['email']

    def clean_password2(self):
        """Check that the two password entries match"""
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class UserChangeForm(ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    disabled password hash display field.

    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = MyUser
        fields = ('email', 'first_name', 'last_name', 'is_active', 'is_admin')
