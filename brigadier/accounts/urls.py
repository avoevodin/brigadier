from django.urls import path
from .views import AccountLoginView, AccountRegistrationView

app_name = 'accounts'
urlpatterns = [
    path('registration/', AccountRegistrationView.as_view(), name='registration'),
    path('login/', AccountLoginView.as_view(), name='login')
]
