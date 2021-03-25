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


class Project(models.Model):
    """Class describes model of the Project entity.

    """
    project_name = models.CharField(verbose_name=_('Project name'), max_length=80)
    description = models.CharField(verbose_name=_('Description'), max_length=400)
    budget = models.FloatField(verbose_name=_('Budget'))
    deadline = models.DateTimeField(verbose_name=_('Deadline'))
    closed = models.BooleanField(verbose_name=_('Closed'))

    def __str__(self):
        return f'{self.project_name}'

    def get_tasks_count(self):
        """Returns amount of tasks of the project.

        """
        return Task.objects.filter(project=self).aggregate(models.Count('id'))

    class Meta:
        verbose_name = _('Project')
        verbose_name_plural = _('Projects')


class Task(models.Model):
    """Class that purpose is describe task structure.

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
        return f'{self.task_name}'

    def author_full_name(self):
        """Returns the full name of the author.

        """
        return self.author.full_name() if self.author else ''

    def assignee_full_name(self):
        """Returns the full name of the assignee.

        """
        return self.assignee.full_name() if self.assignee else ''

    def get_status_repr(self):
        """Returns string representation of the status.

        """
        return STATUSES_DICT[self.status]

    class Meta:
        verbose_name = _('Task')
        verbose_name_plural = _('Tasks')
