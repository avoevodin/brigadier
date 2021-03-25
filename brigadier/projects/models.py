from django.db import models
from django.utils.translation import gettext_lazy as _

from employees.models import Employee

NEW = 'new'
COMPLETED = 'completed'
PROCESSED = 'processed'
STATUSES = [
    (NEW, _('New')),
    (COMPLETED, _('Finished')),
    (PROCESSED, _('Processed')),
]
STATUSES_DICT = dict(STATUSES)


def get_full_name_of_employee(employee):
    """todo()

    """
    if employee is None:
        return ''
    else:
        return employee.full_name()


class Project(models.Model):
    """todo()

    """
    project_name = models.CharField(verbose_name=_('Project name'), max_length=80)
    description = models.CharField(verbose_name=_('Description'), max_length=400)
    budget = models.FloatField(verbose_name=_('Budget'))
    deadline = models.DateTimeField(verbose_name=_('Deadline'))
    closed = models.BooleanField(verbose_name=_('Closed'))

    def __str__(self):
        """todo()

        """
        return f'{self.project_name}'

    class Meta:
        verbose_name = _('Project')
        verbose_name_plural = _('Projects')


class Task(models.Model):
    """todo()

    """
    project = models.ForeignKey(
        Project,
        verbose_name=_('Project'),
        on_delete=models.CASCADE,
    )
    task_name = models.CharField(verbose_name=_('Task name'), max_length=80)
    description = models.CharField(verbose_name=_('Description'), max_length=400)
    start_date = models.DateTimeField(verbose_name=_('Start date'))
    complete_date = models.DateTimeField(verbose_name=_('Complete date'))
    author = models.ForeignKey(
        Employee,
        verbose_name=_('Author'),
        related_name='employee_author',
        null=True,
        on_delete=models.SET_NULL
    )
    assignee = models.ForeignKey(
        Employee,
        verbose_name=_('Assignee'),
        related_name='employee_assignee',
        null=True,
        on_delete=models.SET_NULL
    )
    status = models.CharField(
        verbose_name=_('Status'),
        max_length=20,
        choices=STATUSES,
        default=NEW,

    )

    def __str__(self):
        """todo()

        """
        return f'{self.task_name}'

    def author_full_name(self):
        """todo()

        """
        return get_full_name_of_employee(self.author)

    def assignee_full_name(self):
        """todo()

        """
        return get_full_name_of_employee(self.assignee)

    def get_status_repr(self):
        """todo()

        """
        return STATUSES_DICT[self.status]

    class Meta:
        verbose_name = _('Task')
        verbose_name_plural = _('Tasks')
