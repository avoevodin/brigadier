from django.views import generic
from django.urls import reverse_lazy

from .models import Project, Task
from .forms import ProjectModelForm, TaskModelForm


class ProjectListView(generic.ListView):
    """View displays the list of projects

    """
    model = Project
    template_name = 'project_list.html'
    ordering = 'deadline'


class TaskListView(generic.ListView):
    """View displays the list of tasks.

    """
    model = Task
    template_name = 'task_list.html'
    ordering = 'start_date'


class ProjectDetailView(generic.DetailView):
    """View displays details of the selected project

    """
    model = Project
    template_name = 'project_detail.html'


class TaskDetailView(generic.DetailView):
    """Vies displays detail of the selected
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
