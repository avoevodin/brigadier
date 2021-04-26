from django.conf import settings
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse_lazy, reverse
from django.views import generic

from .forms import ProjectModelForm, TaskModelForm, CommentModelForm
from .models import Project, Task, Comment


class ProjectListView(PermissionRequiredMixin, generic.ListView):
    """View displays the list of projects.

    """
    template_name = 'project_list.html'
    login_url = settings.LOGIN_URL
    permission_required = 'projects.view_project'

    def get_queryset(self):
        """Get objects of Project model with annotating percentage completed,
        selected values and ordered by the deadline field.

        """
        return Project.objects.annotate_completed_percentage().values(
            'id', 'project_name', 'deadline', 'budget', 'closed',
            'tasks_count', 'percentage_completed',
        ).order_by('deadline')


class ProjectDetailView(PermissionRequiredMixin, generic.DetailView):
    """View displays details of the selected project.

    """
    template_name = 'project_detail.html'
    context_object_name = 'project'
    permission_required = 'projects.view_project'

    def get_context_data(self, **kwargs):
        """Extends context data with tasks list of the project.

        """
        project_id = self.kwargs['pk']
        tasks = Task.objects.filter(
            project__id=project_id
        ).select_related(
            'project', 'author', 'assignee'
        )
        context = super(ProjectDetailView, self).get_context_data(**kwargs)
        context['task_list'] = tasks
        return context

    def get_queryset(self, **kwargs):
        """Get object of Project model with annotating percentage completed and
        selected values.

        """
        return Project.objects.annotate_completed_percentage().values(
            'id', 'project_name', 'deadline', 'budget',
            'closed', 'description', 'tasks_count', 'percentage_completed'
        )


class ProjectCreateView(PermissionRequiredMixin, generic.CreateView):
    """View displays creating form of the project.

    """
    model = Project
    template_name = 'project_form.html'
    form_class = ProjectModelForm
    success_url = reverse_lazy('projects:list')
    permission_required = 'projects.add_project'


class ProjectEditView(PermissionRequiredMixin, generic.UpdateView):
    """View displays editing form of the project.

    """
    model = Project
    template_name = 'project_form.html'
    form_class = ProjectModelForm
    permission_required = 'projects.change_project'

    def get_success_url(self):
        """Method returns success url depends of existing next-hook.

        """
        if self.request.GET.get('next'):
            return self.request.GET.get('next')
        else:
            return reverse('projects:list')


class ProjectDeleteView(PermissionRequiredMixin, generic.DeleteView):
    """View displays deleting form of the project.

    """
    model = Project
    template_name = 'project_confirm_delete.html'
    success_url = reverse_lazy('projects:list')
    permission_required = 'projects.delete_project'


class TaskListView(PermissionRequiredMixin, generic.ListView):
    """View displays the list of tasks.

    """
    template_name = 'task_list.html'
    permission_required = 'projects.view_task'

    def get_queryset(self):
        """Extends queryset with related project, author and assignee
        objects. Order queryset by start date.

        """
        return Task.objects.select_related(
            'project', 'author', 'assignee'
        ).order_by('start_date')


class TaskDetailView(PermissionRequiredMixin, generic.DetailView):
    """Vies displays detail of the selected.
    task.

    """
    template_name = 'task_detail.html'
    context_object_name = 'task'
    permission_required = 'projects.view_task'

    def get_queryset(self):
        """Extends objects query-set with related project, author and assignee.

        """
        return Task.objects.select_related('project', 'author', 'assignee')

    def get_context_data(self, **kwargs):
        """Extends context of detail view with comment model form.

        """
        context = super(TaskDetailView, self).get_context_data(**kwargs)
        comment_form = CommentModelForm(initial={'task': self.object})
        context['form'] = comment_form
        return context


class TaskCreateView(PermissionRequiredMixin, generic.CreateView):
    """View displays creating form of the task.

    """
    model = Task
    template_name = 'task_form.html'
    form_class = TaskModelForm
    permission_required = 'projects.add_task'

    def get_success_url(self):
        """Method returns success url depends of existing next-hook.

        """
        if self.request.GET.get('next'):
            return self.request.GET.get('next')
        else:
            return reverse('projects:task_list')


class TaskEditView(PermissionRequiredMixin, generic.UpdateView):
    """View displays editing form of the task.

    """
    model = Task
    template_name = 'task_form.html'
    form_class = TaskModelForm
    permission_required = 'projects.change_task'

    def get_success_url(self):
        """Method returns success url depends of existing next-hook.

        """
        if self.request.GET.get('next'):
            return self.request.GET.get('next')
        else:
            return reverse('projects:task_list')


class TaskDeleteView(PermissionRequiredMixin, generic.DeleteView):
    """View displays deleting form of the task.

    """
    model = Task
    template_name = 'task_confirm_delete.html'
    permission_required = 'projects.delete_task'

    def get_success_url(self):
        """Method returns success url depends of existing next-hook.

        """
        if self.request.GET.get('next'):
            return self.request.GET.get('next')
        else:
            return reverse('projects:task_list')


class CommentCreateView(PermissionRequiredMixin, generic.CreateView):
    """Create view of Comment model.

    """
    model = Comment
    template_name = 'task_detail.html'
    form_class = CommentModelForm
    permission_required = 'projects.add_comment'

    def get_success_url(self):
        """Method returns success url depends of existing next-hook.

        """
        if self.request.GET.get('next'):
            return f"{self.request.GET.get('next')}#{self.object.id}"
        else:
            return reverse('projects:task_list')
