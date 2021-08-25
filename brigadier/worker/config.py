# Celery Configuration Options
timezone = 'Europe/Moscow'
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 30 * 60
result_backend = 'django-db'
cache_backend = 'default'
