from django.urls import path
from .views import (AccountLoginView, AccountRegistrationView,
    AccountRegistrationDoneView, AccountLogoutView)

app_name = 'accounts'
urlpatterns = [
    path('registration/', AccountRegistrationView.as_view(), name='registration'),
    path('registration_done/', AccountRegistrationDoneView.as_view(), name='registration_done'),
    path('login/', AccountLoginView.as_view(), name='login'),
    path('logout/', AccountLogoutView.as_view(), name='logout'),
]

