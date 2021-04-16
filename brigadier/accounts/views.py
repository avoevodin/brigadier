from django.contrib.auth.views import FormView, LoginView
from django.contrib.auth.models import Group
from .forms import AccountRegistrationForm, AccountLoginForm
from django.conf import settings


class AccountRegistrationView(FormView):
    """todo

    """
    form_class = AccountRegistrationForm
    template_name = 'registration.html'
    success_url = settings.LOGIN_URL

    def form_valid(self, form):
        response = super(AccountRegistrationView, self).form_valid(form)
        user = form.save()
        try:
            group_public = Group.objects.get(name='public')
        except Group.DoesNotExist:
            group_public = None
        if group_public is not None:
            user.groups.add(group_public)
        return response


class AccountLoginView(LoginView):
    """todo
    
    """
    form_class = AccountLoginForm
    template_name = 'login.html'
    success_url = settings.LOGIN_REDIRECT_URL
