from django.urls import path

from .views import (AccountLoginView, AccountRegistrationView,
                    AccountRegistrationDoneView, AccountLogoutView,
                    AccountPasswordChangeView, AccountPasswordChangeDoneView,
                    AccountRegistrationActivateView)

app_name = 'accounts'
urlpatterns = [
    path('registration/', AccountRegistrationView.as_view(), name='registration'),
    path('registration_activate/<str:key>/<str:confirm>/', AccountRegistrationActivateView.as_view(), name='registration_activate'),
    path('registration_done/', AccountRegistrationDoneView.as_view(), name='registration_done'),
    path('login/', AccountLoginView.as_view(), name='login'),
    path('logout/', AccountLogoutView.as_view(), name='logout'),
    path('password_change/', AccountPasswordChangeView.as_view(), name='password_change'),
    path('password_change_done/', AccountPasswordChangeDoneView.as_view(), name='password_change_done'),
]

