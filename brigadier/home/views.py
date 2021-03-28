from django.views.generic import TemplateView
from django.utils import timezone
from django.db.models import Count

from projects.models import Project, Task, IN_PROGRESS, COMPLETED
from employees.models import Employee


class HomeView(TemplateView):
    """View of the home page.

    """
    template_name = 'home.html'
    context_object_name = 'statistic_lists'

    def get_context_data(self, **kwargs):
        """Get context data for home page view:
            projects_statistics - statistics of the projects
            tasks_statistics - statistics of the Tasks
            employees_statistics - statistics of the Employees

        """
        projects_statistics = {
            'total': Project.objects.count(),
            'in_progress': Project.objects.filter(closed=False).count(),
            'overdue': Project.objects.filter(
                deadline__lt=timezone.now()
            ).count(),
            'concluded': Project.objects.filter(closed=True).count(),
        }

        tasks_statistics = {
            'total': Task.objects.count(),
            'in_progress': Task.objects.filter(
                status=IN_PROGRESS,
                start_date__gte=timezone.now(),
            ).count(),
            'overdue': Task.objects.filter(
                status=IN_PROGRESS,
                start_date__gte=timezone.now(),
                complete_date__lt=timezone.now(),
            ).count(),
            'concluded': Task.objects.filter(
                status=COMPLETED
            ),
        }

        occupied_employees = Task.objects.filter(
            status=IN_PROGRESS,
            start_date__lte=timezone.now(),
        ).values('assignee').aggregate(
            occupied_employees=Count(
                'assignee',
                distinct=True
            )
        ).get('occupied_employees')
        total_employees = Employee.objects.count()
        overdue_employees = Task.objects.filter(
            status=IN_PROGRESS,
            complete_date__lt=timezone.now(),
        ).values('assignee').aggregate(
            overdue_employees=Count(
                'assignee',
                distinct=True
            )
        ).get('overdue_employees')
        employees_statistics = {
            'total': total_employees,
            'occupied': occupied_employees,
            'no_tasks': total_employees - occupied_employees,
            'overdue_tasks': overdue_employees
            }

        context = super(HomeView, self).get_context_data(**kwargs)
        context['projects_statistics'] = projects_statistics
        context['tasks_statistics'] = tasks_statistics
        context['employees_statistics'] = employees_statistics
        return context
