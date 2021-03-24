from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import Project, Task


class TaskInLine(admin.StackedInline):
    """todo()

    """
    model = Task
    extra = 3
    fields = [
        'id', 'task_name', 'author', 'executor', 'start_date', 'complete_date', 'status'
    ]
    readonly_fields = [
        'id'
    ]
    list_display = [
        'id', 'task_name', 'author', 'executor', 'start_date', 'complete_date', 'status'
    ]
    list_display_links = [
        'id', 'task_name'
    ]
    search_fields = [
        'task_name'
    ]


class ProjectAdmin(admin.ModelAdmin):
    """todo()

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


admin.site.register(Project, ProjectAdmin)
