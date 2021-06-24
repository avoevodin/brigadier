from django.core.mail import send_mail
from django.urls import reverse
from celery import shared_task


@shared_task
def send_veification_mail(host, user_email, key, confirm):
    """todo
    """

    send_mail(
        'Activate your email.',
        f'Hello! \n Your confirmation link for Brigadier account is http://{host}'
        f'{reverse("accounts:registration_activate", args=(key, confirm))}',
        None,
        [user_email]
    )
