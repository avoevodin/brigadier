from django.contrib.auth.views import FormView
from .forms import RegistrationForm


class RegistrationView(FormView):
    """todo

    """
    form_class = RegistrationForm
    template_name = 'registration.html'

