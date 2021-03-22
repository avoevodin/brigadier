from django.views import generic
from django.urls import reverse_lazy

from .forms import EmployeeModelForm

from .models import Employee


class EmployeeListView(generic.ListView):
    """
    todo()
    """
    model = Employee
    template_name = 'employee_list.html'
    ordering = 'id'


class EmployeeDetailView(generic.DetailView):
    """
    todo()
    """
    model = Employee
    template_name = 'employee_detail.html'


class EmployeeCreateView(generic.CreateView):
    """
    todo()
    """
    template_name = 'employee_form.html'
    model = Employee
    form_class = EmployeeModelForm
    success_url = reverse_lazy('employees:list')


class EmployeeEditView(generic.UpdateView):
    """
    todo()
    """
    template_name = 'employee_form.html'
    model = Employee
    form_class = EmployeeModelForm
    success_url = reverse_lazy('employees:list')


class EmployeeDeleteView(generic.DeleteView):
    """
    todo()
    """
    template_name = 'employee_confirm_delete.html'
    model = Employee
    success_url = reverse_lazy('employees:list')
