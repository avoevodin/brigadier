from os import environ as env

from celery import Celery
from worker import config

env.setdefault('DJANGO_SETTINGS_MODULE', 'brigadier.settings')

RABBIT_USER = env.get('RABBITMQ_DEFAULT_USER')
RABBIT_PASS = env.get('RABBITMQ_DEFAULT_PASS')
RABBIT_VHOST = env.get('RABBITMQ_DEFAULT_VHOST')
RABBIT_HOST = env.get('RABBITMQ_HOST')
RABBIT_PORT = env.get('RABBITMQ_PORT')

REDIS_RESULTS_BACKEND = env.get('REDIS_RESULTS_BACKEND', None)

if RABBIT_HOST and RABBIT_PORT and RABBIT_VHOST \
    and RABBIT_PASS and RABBIT_USER:
    broker_url = f'pyamqp://{RABBIT_USER}:{RABBIT_PASS}@' \
        f'{RABBIT_HOST}:{RABBIT_PORT}/{RABBIT_VHOST}'
else:
    broker_url = None # pragma: no cover

app = Celery('worker')

# todo()
# mark it down in the README of the Celery
# app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.broker_url = broker_url

app.conf.result_backend = REDIS_RESULTS_BACKEND

app.config_from_object(config)

app.autodiscover_tasks(['worker'])
