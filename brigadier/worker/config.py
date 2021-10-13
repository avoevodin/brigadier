from celery.schedules import crontab

# Celery Configuration Options
timezone = 'Europe/Moscow'
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 30 * 60
cache_backend = 'default'

beat_schedule = {
    'overdue-notify-every-weekday-midnight': {
        'task': 'worker.email.tasks.create_overdue_notification_tasks',
        'schedule': crontab(hour=12, minute=00, day_of_week='1-5'),
    },
}
