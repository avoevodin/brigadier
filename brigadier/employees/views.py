from django.views import generic
from django.urls import reverse_lazy, reverse

from .forms import EmployeeModelForm

from .models import Employee


class EmployeeListView(generic.ListView):
    """View for the common list of all employees.

    """
    model = Employee
    template_name = 'employee_list.html'
    ordering = 'id'


class EmployeeDetailView(generic.DetailView):
    """Detail view of the concrete employee.

    """
    model = Employee
    template_name = 'employee_detail.html'


class EmployeeCreateView(generic.CreateView):
    """View is responsible for displaying a form that helps to
    create new employees.

    """
    template_name = 'employee_form.html'
    model = Employee
    form_class = EmployeeModelForm
    success_url = reverse_lazy('employees:list')


class EmployeeEditView(generic.UpdateView):
    """View is responsible for displaying a form
    for editing exciting employees.

    """
    template_name = 'employee_form.html'
    model = Employee
    form_class = EmployeeModelForm

    def get_success_url(self):
        """todo

        """
        if self.request.GET.get('next'):
            return self.request.GET.get('next')
        else:
            return reverse('employees:list')


class EmployeeDeleteView(generic.DeleteView):
    """View for the form of deleting employees.

    """
    template_name = 'employee_confirm_delete.html'
    model = Employee

    def get_success_url(self):
        """todo

        """
        if self.request.GET.get('next'):
            return self.request.GET.get('next')
        else:
            return reverse('employees:list')
