from django.contrib import admin

from .models import Employee


class EmployeeAdmin(admin.ModelAdmin):
    """Class that purpose is displaying of Employee in
    the admin-panel.

    """
    fields = [
        'id', 'firstname', 'middlename', 'surname', 'email',
        'user', 'birthdate'
    ]
    readonly_fields = [
        'id'
    ]
    list_display = [
        'id', 'firstname', 'middlename', 'surname', 'email', 'birthdate',
        'user'
    ]
    list_display_links = [
        'id', 'firstname', 'middlename', 'surname'
    ]
    search_fields = [
        'firstname', 'middlename', 'surname', 'user'
    ]
    list_filter = [
        'birthdate'
    ]


admin.site.register(Employee, EmployeeAdmin)
