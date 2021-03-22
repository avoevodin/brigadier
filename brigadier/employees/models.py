from django.db import models
from django.utils.translation import gettext_lazy as _


class Employee(models.Model):
    """
    todo()
    """
    firstname = models.CharField(verbose_name=_('Firstname'), max_length=200)
    middlename = models.CharField(verbose_name=_('Middlename'), max_length=200, null=True, blank=True)
    surname = models.CharField(verbose_name=_('Surname'), max_length=200)
    email = models.EmailField(verbose_name=_('Email'), max_length=200)
    birthdate = models.DateField(verbose_name=_('Birthdate'), null=True, blank=True)

    def __str__(self):
        """
        todo()
        """
        return f'{self.id}: {self.full_name()}'

    def full_name(self):
        """
        todo()
        """
        return f'{self.firstname} {self.middlename} {self.surname}'
    full_name.short_description = _('Full name')

