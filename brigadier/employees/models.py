from django.db import models
from django.utils.translation import gettext_lazy as _


class Employee(models.Model):
    """Class is used for model Employee (saving, updating, deleting).

    """
    firstname = models.CharField(
        verbose_name=_('Firstname'),
        max_length=200,
    )
    middlename = models.CharField(
        verbose_name=_('Middlename'),
        max_length=200,
        null=True,
        blank=True,
    )
    surname = models.CharField(
        verbose_name=_('Surname'),
        max_length=200,
    )
    email = models.EmailField(verbose_name=_('Email'), max_length=200)
    birthdate = models.DateField(
        verbose_name=_('Birthdate'),
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.full_name()

    def full_name(self):
        """Returns full name of an employee. Contains from
        a first name, a middle name if it exists and a surname,
        that are separated with spaces.

        """
        return " ".join([self.firstname, self.middlename, self.surname]).replace("  ", " ").strip()
    full_name.short_description = _('Full name')

    class Meta:
        verbose_name = _('Employee')
        verbose_name_plural = _('Employees')
