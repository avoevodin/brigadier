from django.views import generic
from django.urls import reverse_lazy
from django.db.models import Count, Q, FloatField
from django.db.models.functions import Cast

from .models import Project, Task, COMPLETED
from .forms import ProjectModelForm, TaskModelForm


def annotate_completed_percentage(field_list):
    """todo()

    """
    return Project.objects.values(*field_list).annotate(
            tasks_count=Count('task'),
            percentage_completed=Cast(Count(
                'task',
                filter=Q(task__status=COMPLETED),
            ), FloatField()) / Cast(Count('task'), FloatField()) * 100
        )


class ProjectListView(generic.ListView):
    """View displays the list of projects.

    """
    template_name = 'project_list.html'

    def get_queryset(self):
        """todo()

        """
        return annotate_completed_percentage(
            ['id', 'project_name', 'deadline', 'budget', 'closed']
        ).order_by('deadline')


class TaskListView(generic.ListView):
    """View displays the list of tasks.

    """
    model = Task
    template_name = 'task_list.html'
    ordering = 'start_date'


class ProjectDetailView(generic.DetailView):
    """View displays details of the selected project.

    """
    template_name = 'project_detail.html'

    def get_queryset(self):
        """todo()

        """
        return annotate_completed_percentage(
            ['id', 'project_name', 'deadline', 'budget', 'closed', 'description']
        )


class TaskDetailView(generic.DetailView):
    """Vies displays detail of the selected.
    task.

    """
    model = Task
    template_name = 'task_detail.html'


class ProjectCreateView(generic.CreateView):
    """View displays creating form of the project.

    """
    model = Project
    template_name = 'project_form.html'
    form_class = ProjectModelForm
    success_url = reverse_lazy('projects:list')


class ProjectEditView(generic.UpdateView):
    """View displays editing form of the project.

    """
    model = Project
    template_name = 'project_form.html'
    form_class = ProjectModelForm
    success_url = reverse_lazy('projects:list')


class ProjectDeleteView(generic.DeleteView):
    """View displays deleting form of the project.

    """
    model = Project
    template_name = 'project_confirm_delete.html'
    success_url = reverse_lazy('projects:list')


class TaskCreateView(generic.CreateView):
    """View displays creating form of the task.

    """
    model = Task
    template_name = 'task_form.html'
    form_class = TaskModelForm
    success_url = reverse_lazy('projects:task_list')


class TaskEditView(generic.UpdateView):
    """View displays editing form of the task.

    """
    model = Task
    template_name = 'task_form.html'
    form_class = TaskModelForm
    success_url = reverse_lazy('projects:task_list')


class TaskDeleteView(generic.DeleteView):
    """View displays deleting form of the task.

    """
    model = Task
    template_name = 'task_confirm_delete.html'
