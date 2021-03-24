from django.contrib import admin

from .models import Employee


class EmployeeAdmin(admin.ModelAdmin):
    """todo()'

    """
    fields = [
        'id', 'firstname', 'middlename', 'surname', 'email', 'birthdate'
    ]
    readonly_fields = [
        'id'
    ]
    list_display = [
        'id', 'firstname', 'middlename', 'surname', 'email', 'birthdate'
    ]
    list_display_links = [
        'id', 'firstname', 'middlename', 'surname'
    ]
    search_fields = [
        'firstname', 'middlename', 'surname'
    ]
    list_filter = [
        'birthdate'
    ]


admin.site.register(Employee, EmployeeAdmin)
