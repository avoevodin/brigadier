from django.contrib.auth.views import (FormView, LoginView,
                                       TemplateView, LogoutView,
                                       PasswordChangeView, PasswordChangeDoneView)
from django.contrib.auth.models import Group, User
from django.urls import reverse_lazy, reverse
from .forms import AccountRegistrationForm, AccountLoginForm, AccountPasswordChangeForm
from django.conf import settings
from uuid import uuid4
from django.core.mail import send_mail
from django.core.cache import cache
from django.contrib.sites.shortcuts import get_current_site


class AccountRegistrationView(FormView):
    """Account registration view. If the public group exist it will be
    added to user account by default.

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
        cache.set(key, data, settings.EXPIRE_LINK)
        host = get_current_site(self.request)
        send_mail(
            'Activate your email.',
            f'Hello, link http://{host}'
            f'{reverse("accounts:registration_activate", args=(key, confirm))}',
            None,
            [user.email]
        )

        try:
            group_public = Group.objects.get(name='public')
            user.groups.add(group_public)
        except Group.DoesNotExist:
            pass
        return response


class AccountRegistrationDoneView(TemplateView):
    """Registration view.

    """
    template_name = 'registration_done.html'


class AccountRegistrationActivateView(TemplateView):
    """todo

    """
    template_name = 'registration_activate.html'

    def get_context_data(self, **kwargs):
        context = super(AccountRegistrationActivateView, self).get_context_data(**kwargs)
        key = kwargs.get('key')
        confirm = kwargs.get('confirm')
        data = cache.get(key)
        if (data is not None) and (data.get('confirm'))\
            and (data.get('confirm') == confirm):
            user = User.objects.get(pk=data.get('user_id'))
            user.is_active = True
            user.save()
            context['message'] = 'ok'
        context['message'] = 'error'
        return context


class AccountLoginView(LoginView):
    """Loging view.
    
    """
    form_class = AccountLoginForm
    template_name = 'login.html'
    success_url = settings.LOGIN_REDIRECT_URL


class AccountLogoutView(LogoutView):
    """Logout view.

    """
    next_page = settings.LOGIN_URL


class AccountPasswordChangeView(PasswordChangeView):
    """Password change view.

    """
    form_class = AccountPasswordChangeForm
    template_name = 'password_change.html'
    success_url = reverse_lazy('accounts:password_change_done')


class AccountPasswordChangeDoneView(PasswordChangeDoneView):
    """Password change done view.

    """
    template_name = 'password_change_done.html'
