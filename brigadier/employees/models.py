from django.db import models
from django.utils.translation import gettext_lazy as _


class Employee(models.Model):
    """Class describes an employee entity.

    """
    firstname = models.CharField(verbose_name=_('Firstname'), max_length=200)
    middlename = models.CharField(
            verbose_name=_('Middlename'),
            max_length=200,
            null=True,
            blank=True,
        )
    surname = models.CharField(verbose_name=_('Surname'), max_length=200)
    email = models.EmailField(verbose_name=_('Email'), max_length=200)
    birthdate = models.DateField(
        verbose_name=_('Birthdate'),
        null=True,
        blank=True,
    )

    def __str__(self):
        return f'{self.id}: {self.full_name()}'

    def full_name(self):
        """Returns full name of an employee. Contains from
        a first name, a middle name if it exists and a surname,
        that are separated with spaces.

        """
        return f'{self.firstname} {self.middlename if self.middlename else ""} {self.surname}'
    full_name.short_description = _('Full name')
