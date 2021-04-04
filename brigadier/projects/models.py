from django.db import models
from django.utils.translation import gettext_lazy as _
from django.db.models import Case, When, Count, Q, FloatField, DecimalField
from django.db.models.functions import Cast

from employees.models import Employee

NEW = 'new'
COMPLETED = 'completed'
IN_PROGRESS = 'in_progress'
STATUSES = [
    (NEW, _('New')),
    (COMPLETED, _('Finished')),
    (IN_PROGRESS, _('In progress')),
]
STATUSES_DICT = dict(STATUSES)


class ProjectManager(models.Manager):
    """todo()

    """

    def annotate_completed_percentage(self):
        """todo()

        """
        return self.annotate(
            tasks_count=Count('task'),
            percentage_completed=Case(
                When(tasks_count=0, then=0),
                default=Cast(
                    Count(
                        'task',
                        filter=Q(task__status=COMPLETED),
                    ), FloatField()) / Cast(Count('task'), FloatField()),
            ) * 100
        )


class Project(models.Model):
    """Class describes model of the Project entity.

    """
    project_name = models.CharField(verbose_name=_('Project name'), max_length=80)
    description = models.TextField(verbose_name=_('Description'), max_length=400, blank=True)
    budget = models.FloatField(verbose_name=_('Budget'))
    deadline = models.DateTimeField(verbose_name=_('Deadline'))
    closed = models.BooleanField(verbose_name=_('Closed'), null=False, blank=False)

    objects = ProjectManager()

    def __str__(self):
        return f'{self.project_name}'

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
    description = models.TextField(
        verbose_name=_('Description'),
        max_length=400,
        blank=True,
        null=True
    )
    start_date = models.DateTimeField(verbose_name=_('Start date'))
    complete_date = models.DateTimeField(verbose_name=_('Complete date'))
    author = models.ForeignKey(
        Employee,
        verbose_name=_('Author'),
        related_name='tasks_author',
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    assignee = models.ForeignKey(
        Employee,
        verbose_name=_('Assignee'),
        related_name='tasks_assignee',
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    status = models.CharField(
        verbose_name=_('Status'),
        max_length=20,
        choices=STATUSES,
        default=NEW,
    )

    def get_status_repr(self):
        """Returns string representation of the status.

        """
        return STATUSES_DICT[self.status]

    def __str__(self):
        return f'{self.task_name}'

    class Meta:
        verbose_name = _('Task')
        verbose_name_plural = _('Tasks')


class Comment(models.Model):
    """todo

    """
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        verbose_name=_('Task'),
        related_name='comments',
    )
    created_date = models.DateTimeField(
        verbose_name=_('Date of creating'),
        auto_now_add=True,
    )
    text = models.TextField(verbose_name=_('Text'), max_length=200)

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = _('Comment')
        verbose_name_plural = _('Comments')
