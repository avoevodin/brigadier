from django.core.mail import send_mail
from django.urls import reverse
from worker.app import app


@app.task(
    max_retries=5,
    default_retry_delay=60,
    auto_retry_for=(ConnectionRefusedError,)
)
def send_verification_mail(host, user_email, key, confirm):
    """todo
    """

    send_mail(
        'Activate your email.',
        f'Hello! \n Your confirmation link for Brigadier account is http://{host}'
        f'{reverse("accounts:registration_activate", args=(key, confirm))}',
        None,
        [user_email]
    )


@app.task
def debug_task(self):
    print(f'Request: {self.request!r}')
