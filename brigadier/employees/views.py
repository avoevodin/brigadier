from django.shortcuts import render
from django.views import generic

from .models import Employee


class EmployeeListView(generic.ListView):
    """
    todo()
    """
    model = Employee
    template_name = 'employee_list.html'


class EmployeeDetailView(generic.DetailView):
    """
    todo()
    """
    model = Employee
    template_name = 'employee_detail.html'
