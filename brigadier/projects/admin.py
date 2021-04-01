from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import Project, Task, Comment


class TaskInLine(admin.StackedInline):
    """Class based on the inline model that serves for inline displaying of
    tasks in projects.

    """
    model = Task
    extra = 3
    fields = [
        'id', 'task_name', 'author', 'assignee', 'start_date', 'complete_date', 'status'
    ]
    readonly_fields = [
        'id'
    ]
    list_display = [
        'id', 'task_name', 'author', 'assignee', 'start_date', 'complete_date', 'status'
    ]
    list_display_links = [
        'id', 'task_name'
    ]
    search_fields = [
        'task_name'
    ]


class CommentInline(admin.TabularInline):
    """todo

    """
    model = Comment
    extra = 1
    fields = [
        'id', 'task', 'created_date', 'text'
    ]
    readonly_fields = [
        'id', 'created_date'
    ]
    list_display = [
        'id', 'task', 'created_date', 'text'
    ]
    list_display_links = [
        'id', 'task'
    ]
    search_fields = [
        'task', 'text'
    ]


class ProjectAdmin(admin.ModelAdmin):
    """Class based on the admin model. Its purpose is
    displaying projects in the admin panel.

    """
    fieldsets = [
        (None, {
            'fields': ['id', 'project_name', 'deadline', 'budget', 'closed']
        }),
        (_('Description'), {'fields': ['description']})
    ]
    readonly_fields = [
        'id'
    ]
    list_display = [
       'id', 'project_name', 'deadline', 'budget', 'closed'
    ]
    list_display_links = [
        'id', 'project_name'
    ]
    search_fields = [
        '^project_name'
    ]
    list_filter = [
        'deadline'
    ]
    inlines = [TaskInLine]


class TaskAdmin(admin.ModelAdmin):
    """Class based on the admin model. Its purpose is
    displaying tasks in the admin panel.

    """
    model = Task
    fieldsets = [
        (None, {
            'fields': ['id', 'task_name', 'author', 'assignee']
        }),
        (_('Terms and status'), {
            'fields': ['start_date', 'complete_date', 'status']
        }),
        (_('Description'), {'fields': ['description']})
    ]
    readonly_fields = [
        'id'
    ]
    list_display = [
        'id', 'task_name', 'author', 'assignee',
        'start_date', 'complete_date', 'status',
    ]
    list_display_links = [
        'id', 'task_name'
    ]
    search_fields = [
        'task_name'
    ]
    list_filter = [
        'start_date', 'complete_date'
    ]
    inlines = [CommentInline]


class CommentAdmin(admin.ModelAdmin):
    """todo

    """
    model = Comment
    fieldsets = [
        (None, {
            'fields': ['id', 'task', 'created_date']
        }),
        (_('Text'), {
            'fields': ['text']
        }),
    ]
    readonly_fields = [
        'id', 'created_date',
    ]
    list_display = [
        'id', 'task', 'created_date', 'text',
    ]
    list_display_links = [
        'id', 'task',
    ]
    search_fields = [
        'task', 'text',
    ]
    list_filter = [
        'created_date',
    ]


admin.site.register(Project, ProjectAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(Comment, CommentAdmin)
