from os import environ

from celery import Celery

environ.setdefault('DJANGO_SETTINGS_MODULE', 'brigadier.settings')

app = Celery('brigadier')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

@app.task
def debug_task(self):
    print(f'Request: {self.request!r}')
