from django.views import generic
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import PermissionRequiredMixin

from .forms import EmployeeModelForm

from .models import Employee


class EmployeeListView(PermissionRequiredMixin, generic.ListView):
    """View for the common list of all employees.

    """
    model = Employee
    template_name = 'employee_list.html'
    ordering = 'id'
    permission_required = 'employees.view_employee'


class EmployeeDetailView(PermissionRequiredMixin, generic.DetailView):
    """Detail view of the concrete employee.

    """
    model = Employee
    template_name = 'employee_detail.html'
    permission_required = 'employees.view_employee'


class EmployeeCreateView(PermissionRequiredMixin, generic.CreateView):
    """View is responsible for displaying a form that helps to
    create new employees.

    """
    template_name = 'employee_form.html'
    model = Employee
    form_class = EmployeeModelForm
    success_url = reverse_lazy('employees:list')
    permission_required = 'employees.add_employee'


class EmployeeEditView(PermissionRequiredMixin, generic.UpdateView):
    """View is responsible for displaying a form
    for editing exciting employees.

    """
    template_name = 'employee_form.html'
    model = Employee
    form_class = EmployeeModelForm
    permission_required = 'employees.change_employee'

    def get_success_url(self):
        """Method returns success url depends of existing next-hook.

        """
        if self.request.GET.get('next'):
            return self.request.GET.get('next')
        else:
            return reverse('employees:list')


class EmployeeDeleteView(PermissionRequiredMixin, generic.DeleteView):
    """View for the form of deleting employees.

    """
    template_name = 'employee_confirm_delete.html'
    model = Employee
    success_url = reverse_lazy('employees:list')
    permission_required = 'employees.delete_employee'
