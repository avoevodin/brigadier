from django.views.generic import TemplateView
from django.utils import timezone
from django.db.models import Count, Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings

from projects.models import Project, Task, IN_PROGRESS, COMPLETED, NEW
from employees.models import Employee


class HomeView(LoginRequiredMixin, TemplateView):
    """View of the home page.

    """
    login_url = settings.LOGIN_URL
    template_name = 'home.html'
    context_object_name = 'statistic_lists'

    def get_context_data(self, **kwargs):
        """Get context data for home page view:
            projects_statistics - statistics of the projects
            tasks_statistics - statistics of the Tasks
            employees_statistics - statistics of the Employees

        """
        projects_statistics = Project.objects.aggregate(
            total=Count('id'),
            in_progress=Count('id', filter=Q(closed=False)),
            overdue=Count('id', filter=Q(closed=False, deadline__lt=timezone.now())),
            done=Count('id', filter=Q(closed=True)),
        )
        tasks_statistics = Task.objects.aggregate(
            total=Count('id'),
            in_progress=Count(
                'id',
                filter=Q(
                    status=IN_PROGRESS,
                    start_date__lte=timezone.now()
                )
            ),
            overdue=Count(
                'id', filter=Q(
                    status=IN_PROGRESS,
                    complete_date__lt=timezone.now()
                )
            ),
            done=Count('id', filter=Q(status=COMPLETED)),
            new=Count('id', filter=Q(status=NEW)),
        )
        employees_statistics = Employee.objects.aggregate(
            total=Count('id', distinct=True),
            occupied=Count(
                'tasks_assignee__assignee',
                filter=Q(
                    tasks_assignee__status=IN_PROGRESS,
                    tasks_assignee__start_date__lte=timezone.now()
                ),
                distinct=True
            ),
            overdue=Count(
                'tasks_assignee__assignee',
                filter=Q(
                    tasks_assignee__status=IN_PROGRESS,
                    tasks_assignee__complete_date__lte=timezone.now()
                ),
                distinct=True
            ),
            no_tasks=Count('id', distinct=True) - Count(
                'tasks_assignee__assignee',
                filter=Q(
                    tasks_assignee__status=IN_PROGRESS,
                    tasks_assignee__start_date__lte=timezone.now()
                ),
                distinct=True
            ),
        )
        context = super(HomeView, self).get_context_data(**kwargs)
        context['projects_statistics'] = projects_statistics
        context['tasks_statistics'] = tasks_statistics
        context['employees_statistics'] = employees_statistics
        return context
