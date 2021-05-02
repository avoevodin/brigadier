from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, UserManager, AbstractUser, PermissionsMixin
from django.contrib.auth.hashers import make_password
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.core.mail import send_mail
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.apps import apps


class MyUserManager(BaseUserManager):
    """todo

    """

    def _create_user(self, username, email, password, **extra_fields):
        """todo

        """
        if not username or not email:
            raise ValueError(_('Users must have a username and an email address'))

        GlobalUserModel = apps.get_model(self.model._meta.app_label, self.model._meta.object_name)
        user = self.model(
            email=self.normalize_email(email),
            username=GlobalUserModel.normalize_username(username),
            password=make_password(password),
            **extra_fields,
        )
        user.save(using=self._db)
        return user

    def create_user(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_admin', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email, password, **extra_fields):
        """todo

        """
        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_admin') is not True:
            raise ValueError(_('Superuser must have is_admin=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        return self._create_user(username, email, password, **extra_fields)


class MyUser(AbstractBaseUser, PermissionsMixin):
    """todo

    """
    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    first_name = models.CharField(_('first name'), max_length=150, blank=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True)
    email = models.EmailField(
        _('email address'),
        blank=True,
        max_length=255,
        unique=True,
    )
    is_admin = models.BooleanField(
        _('admin status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta(AbstractBaseUser.Meta):
        swappable = 'AUTH_USER_MODEL'
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        """Return the first_name plus the last_name, with a space in between.

        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)

    # @property
    # def is_staff(self):
    #     """Is the user a member of staff?"""
    #     return self.is_admin
