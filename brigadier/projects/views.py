from django.views import generic
from django.urls import reverse_lazy, reverse

from .models import Project, Task, Comment
from .forms import ProjectModelForm, TaskModelForm, CommentModelForm


class ProjectListView(generic.ListView):
    """View displays the list of projects.

    """
    template_name = 'project_list.html'

    def get_queryset(self):
        """todo()

        """
        return Project.objects.annotate_completed_percentage().values(
            'id', 'project_name', 'deadline', 'budget', 'closed',
            'tasks_count', 'percentage_completed',
        ).order_by('deadline')

    def get_context_data(self, **kwargs):
        """todo()

        """
        context = super(ProjectListView, self).get_context_data(**kwargs)
        context['next'] = reverse_lazy('projects:list')
        return context


class TaskListView(generic.ListView):
    """View displays the list of tasks.

    """
    template_name = 'task_list.html'

    def get_queryset(self):
        """todo

        """
        return Task.objects.select_related(
            'project', 'author', 'assignee'
        ).order_by('start_date')

    def get_context_data(self, **kwargs):
        """todo

        """
        context = super(TaskListView, self).get_context_data(**kwargs)
        context['next'] = reverse_lazy('projects:task_list')
        return context


class ProjectDetailView(generic.DetailView):
    """View displays details of the selected project.

    """
    template_name = 'project_detail.html'
    context_object_name = 'project'

    def get_context_data(self, **kwargs):
        """todo()

        """
        project_id = self.kwargs['pk']
        tasks = Task.objects.filter(
            project__id=project_id
        ).select_related(
            'project', 'author', 'assignee'
        )
        context = super(ProjectDetailView, self).get_context_data(**kwargs)
        context['task_list'] = tasks
        context['next'] = reverse_lazy(
            'projects:detail',
            kwargs={'pk': project_id}
        )
        return context

    def get_queryset(self, **kwargs):
        """todo()

        """
        return Project.objects.annotate_completed_percentage().values(
            'id', 'project_name', 'deadline', 'budget',
            'closed', 'description', 'tasks_count', 'percentage_completed'
        )


class TaskDetailView(generic.DetailView):
    """Vies displays detail of the selected.
    task.

    """
    template_name = 'task_detail.html'
    context_object_name = 'task'

    def get_queryset(self):
        """todo

        """
        return Task.objects.select_related('project', 'author', 'assignee')

    def get_context_data(self, **kwargs):
        """todo()

        """
        task_id = self.kwargs['pk']
        context = super(TaskDetailView, self).get_context_data(**kwargs)
        context['next'] = reverse_lazy(
            'projects:task_detail',
            kwargs={'pk': task_id}
        )
        return context


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

    def get_success_url(self):
        """todo()

        """
        if self.request.GET.get('next'):
            return self.request.GET.get('next')
        else:
            return reverse('projects:list')


class ProjectDeleteView(generic.DeleteView):
    """View displays deleting form of the project.

    """
    model = Project
    template_name = 'project_confirm_delete.html'

    def get_success_url(self):
        """todo()

        """
        if self.request.GET.get('next'):
            return self.request.GET.get('next')
        else:
            return reverse('projects:list')


class TaskCreateView(generic.CreateView):
    """View displays creating form of the task.

    """
    model = Task
    template_name = 'task_form.html'
    form_class = TaskModelForm

    def get_success_url(self):
        """todo

        """
        if self.request.GET.get('next'):
            return self.request.GET.get('next')
        else:
            return reverse('projects:task_list')


class TaskEditView(generic.UpdateView):
    """View displays editing form of the task.

    """
    model = Task
    template_name = 'task_form.html'
    form_class = TaskModelForm
    success_url = reverse_lazy('projects:task_list')

    def get_success_url(self):
        """todo

        """
        if self.request.GET.get('next'):
            return self.request.GET.get('next')
        else:
            return reverse('projects:task_list')


class TaskDeleteView(generic.DeleteView):
    """View displays deleting form of the task.

    """
    model = Task
    template_name = 'task_confirm_delete.html'

    def get_success_url(self):
        """todo

        """
        if self.request.GET.get('next'):
            return self.request.GET.get('next')
        else:
            return reverse('projects:task_list')


class CommentCreateView(generic.CreateView):
    """todo

    """
    model = Comment
    template_name = 'comment_form.html'
    form_class = CommentModelForm

    def get_success_url(self):
        """todo

        """
        if self.request.GET.get('next'):
            return self.request.GET.get('next')
        else:
            return reverse('projects:task_detail')
