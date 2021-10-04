from uuid import uuid4

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.auth.views import (FormView, LoginView,
                                       TemplateView, LogoutView,
                                       PasswordChangeView, PasswordChangeDoneView)
from django.contrib.sites.shortcuts import get_current_site
from django.core.cache import cache
from django.urls import reverse_lazy

from .forms import AccountRegistrationForm, AccountLoginForm, AccountPasswordChangeForm
from worker.email.tasks import send_verification_mail, send_onboarding_mail

User = get_user_model()


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
        host = get_current_site(self.request).domain
        send_verification_mail.delay(host, user.email, key, confirm)

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
    """View for activate users from link. This link
    is sent to user's email.

    """
    template_name = 'registration_activate.html'

    def get_context_data(self, **kwargs):  # pragma: no cover
        context = super(AccountRegistrationActivateView, self).get_context_data(**kwargs)
        key = kwargs.get('key')
        confirm = kwargs.get('confirm')
        data = cache.get(key)
        if (data is not None) and (data.get('confirm')) \
                and (data.get('confirm') == confirm):
            user = User.objects.get(pk=data.get('user_id'))
            user.is_active = True
            user.save()
            context['message'] = 'ok'

            host = get_current_site(self.request).domain
            send_onboarding_mail(host, user.email)
        else:
            context['message'] = 'error'
        return context


class AccountRegistrationActivationDoneView(TemplateView):
    """todo
    """
    template_name = "registration_activation_done.html"


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
