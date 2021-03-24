from django.views import generic
from django.urls import reverse_lazy

from .models import Project, Task
from .forms import  ProjectModelForm, TaskModelForm

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


class ProjectCreateView(generic.CreateView):
    """todo()

    """
    model = Project
    template_name = 'project_form.html'
    form_class = ProjectModelForm
    success_url = reverse_lazy('projects:list')


class ProjectEditView(generic.UpdateView):
    """todo()

    """
    model = Project
    template_name = 'project_form.html'
    form_class = ProjectModelForm
    success_url = reverse_lazy('projects:list')


class ProjectDeleteView(generic.DeleteView):
    """todo()

    """
    model = Project
    template_name = 'project_confirm_delete.html'
    success_url = reverse_lazy('projects:list')


class TaskCreateView(generic.CreateView):
    """todo()

    """
    model = Task
    template_name = 'task_form.html'
    form_class = TaskModelForm
    success_url = reverse_lazy('projects:task_list')
