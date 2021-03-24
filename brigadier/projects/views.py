from django.views import generic

from .models import Project, Task


class ProjectListView(generic.ListView):
    """todo()

    """
    model = Project
    template_name = 'project_list.html'
    ordering = 'deadline'


class TaskListView(generic.ListView):
    """todo()

    """
    model = Task
    template_name = 'task_list.html'
    ordering = 'start_date'


class ProjectDetailView(generic.DetailView):
    """todo()

    """
    model = Project
    template_name = 'project_detail.html'

class TaskDetailView(generic.DetailView):
    """todo()

    """
    model = Task
    template_name = 'task_detail.html'
