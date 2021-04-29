from django.contrib.auth.views import (FormView, LoginView,
                                       TemplateView, LogoutView,
                                       PasswordChangeView, PasswordChangeDoneView)
from django.contrib.auth.models import Group
from django.urls import reverse_lazy
from django.conf import settings
from django.core.cache import cache
from uuid import uuid4
from django.utils.translation import gettext as _
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site

from .forms import AccountRegistrationForm, AccountLoginForm, AccountPasswordChangeForm


class AccountRegistrationView(FormView):
    """todo

    """
    form_class = AccountRegistrationForm
    template_name = 'registration.html'
    success_url = reverse_lazy("accounts:registration_done")

    def form_valid(self, form):
        response = super(AccountRegistrationView, self).form_valid(form)
        user = form.save(commit=False)
        user.is_active = False
        user.save()

        key = uuid4().hex
        confirm = uuid4().hex
        data = {
            'confirm': confirm,
            'user_id': user.id,
        }
        cache.set(key, data, settings.EXPIRE_ACTIVATION_LINK)
        host = get_current_site(self.request)
        send_mail(_('Activate your email'), _(f'Hello, link http://{host}/{key}/{confirm}'),
                  None, [user.email])

        try:
            group_public = Group.objects.get(name='public')
            user.groups.add(group_public)
        except Group.DoesNotExist:
            pass
        return response


class AccountRegistrationDoneView(TemplateView):
    """todo

    """
    template_name = 'registration_done.html'


class AccountRegistrationActivateView(TemplateView):
    """todo

    """



class AccountLoginView(LoginView):
    """todo
    
    """
    form_class = AccountLoginForm
    template_name = 'login.html'
    success_url = settings.LOGIN_REDIRECT_URL


class AccountLogoutView(LogoutView):
    """todo

    """
    next_page = settings.LOGIN_URL


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
