from django.contrib.auth.views import FormView
from django.contrib.auth.models import Group
from django.urls import reverse
from .forms import RegistrationForm
from django.conf import settings


class RegistrationView(FormView):
    """todo

    """
    form_class = RegistrationForm
    template_name = 'registration.html'
    success_url = settings.LOGIN_REDIRECT_URL

    def form_valid(self, form):
        response = super(RegistrationView, self).form_valid(form)
        user = form.save()
        try:
            group_public = Group.objects.get(name='public')
        except Group.DoesNotExist:
            group_public = None
        if group_public is not None:
            user.groups.add(group_public)
        return response
