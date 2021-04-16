from django.contrib.auth.views import (FormView, LoginView,
                                       TemplateView, LogoutView,
                                       PasswordChangeView, PasswordChangeDoneView)
from django.contrib.auth.models import Group
from django.urls import reverse_lazy
from .forms import AccountRegistrationForm, AccountLoginForm, AccountPasswordChangeForm
from django.conf import settings


class AccountRegistrationView(FormView):
    """todo

    """
    form_class = AccountRegistrationForm
    template_name = 'registration.html'
    success_url = reverse_lazy("accounts:registration_done")

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


class AccountRegistrationDoneView(TemplateView):
    """todo

    """
    template_name = 'registration_done.html'


class AccountLoginView(LoginView):
    """todo
    
    """
    form_class = AccountLoginForm
    template_name = 'login.html'
    success_url = settings.LOGIN_REDIRECT_URL


class AccountLogoutView(LogoutView):
    """todo

    """
    success_url = settings.LOGIN_URL


class AccountPasswordChangeView(PasswordChangeView):
    """todo

    """
    form_class = AccountPasswordChangeForm
    template_name = 'password_change.html'
    success_url = reverse_lazy('accounts:password_change_done')


class AccountPasswordChangeDoneView(PasswordChangeDoneView):
    """todo

    """
    template_name = 'password_change_done.html'
