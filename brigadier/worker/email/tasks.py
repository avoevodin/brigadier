from celery.schedules import crontab
from django.core.mail import send_mail
from django.db.models import F
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext as _
from projects.models import Task, IN_PROGRESS
from worker.app import app


def get_overdue_emails():
    """Get overdue emails texts sorted by user's emails.

    """
    overdue_tasks_qs = Task.objects.filter(
        status=IN_PROGRESS, complete_date__lt=timezone.now() - timezone.timedelta(hours=1)).annotate(
        user_email=F('assignee__user__email'),
        task_id=F('id')
    ).order_by('user_email').values(
        'task_name', 'task_id', 'user_email', 'complete_date'
    )
    overdue_tasks = []
    for task_data in overdue_tasks_qs:
        overdue_delta = timezone.now() - task_data.get('complete_date')
        overdue_days = str(overdue_delta.days)
        overdue_hours = str(overdue_delta.seconds // 3600)
        overdue_tasks += [{
            'task_name': task_data.get('task_name'),
            'task_id': task_data.get('task_id'),
            'user_email': task_data.get('user_email'),
            'overdue_days': overdue_days,
            'overdue_hours': overdue_hours,
        }]

    overdue_emails = []
    user_tasks_list_str = ''
    group_email = ''
    for task_data in overdue_tasks:
        current_email = task_data.get('user_email')
        if group_email and group_email != current_email:
            overdue_emails += [{
                'email': group_email,
                'tasks_list_str': user_tasks_list_str
            }]
            group_email = current_email
            user_tasks_list_str = ''
        elif not group_email:
            group_email = current_email

        user_tasks_list_str += _(f'Task "') + task_data.get('task_name') \
                               + _(f'" overdue for ') + task_data.get('overdue_days') + _(f' days ') \
                               + _(f'and ') + task_data.get('overdue_hours') + _(f' hours.\n')

    if user_tasks_list_str:
        overdue_emails += [{
            'email': group_email,
            'tasks_list_str': user_tasks_list_str
        }]

    return overdue_emails


@app.task(
    max_retries=5,
    default_retry_delay=60,
    auto_retry_for=(ConnectionRefusedError,)
)
def send_verification_mail(host, user_email, key, confirm):
    """Sending verification mail with verification link to
    confirm user's registration process.

    """
    send_mail(
        _('Activate your account.'),
        _(f'Hello!\nYour confirmation link for Brigadier account is\n')
        + f'http://{host}'
          f'{reverse("accounts:registration_activate", args=(key, confirm))}',
        None,
        [user_email]
    )


@app.task(
    max_retries=5,
    default_retry_delay=60,
    auto_retry_for=(ConnectionRefusedError,)
)
def send_onboarding_mail(host, user_email):
    """Sending onboarding mail to user who finished registration
    successfully.

    """
    send_mail(
        _('Welcome!'),
        _(
            f'Brigadier team welcomes you on board and we wish you a productive work.\n'
            f'To help you achieve productivity take a tour:\n'
        ) + f'http://{host}'
            f'{reverse("accounts:registration_activation_done")}',
        None,
        [user_email]
    )


@app.task(
    max_retries=5,
    default_retry_delay=60,
    auto_retry_for=(ConnectionRefusedError,)
)
def create_overdue_notification_tasks():
    """Task creates tasks for sending overdue notification emails.

    """
    overdue_emails = get_overdue_emails()

    for overdue_data in overdue_emails:
        send_overdue_notification_email.delay(
            overdue_data.get('email'),
            overdue_data.get('tasks_list_str')
        )


@app.task(
    max_retries=5,
    default_retry_delay=60,
    auto_retry_for=(ConnectionRefusedError,)
)
def send_overdue_notification_email(user_email, overdue_tasks_list):
    """Task sends overdue notification email.

    """
    send_mail(
        _('Hello!'),
        _(f'Seems that you have some overdue tasks here:\n')
        + overdue_tasks_list,
        None,
        [user_email]
    )


@app.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    """Periodic task for sending notifications about overdue tasks.

    """
    sender.add_periodic_task(
        crontab(hour=12, minute=00, day_of_week='1-5'),
        create_overdue_notification_tasks.s(),
        name='Overdue notifications from Monday to Friday at 12:00.'
    )  # pragma: no cover


@app.task
def debug_task(self):
    print(f'Request: {self.request!r}')  # pragma: no cover
