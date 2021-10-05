# Tutorial for Celery

## Just Celery

### Choose and run the broker
* Run RabbitMQ image from the Docker
```shell
docker run -d --name celery-test-rabbitmq \
--hostname celery-test-rabbitmq -p 5672:5672 rabbitmq 
```

### Install Celery
```shell
pip install celery
```

### Create Celery app
* Example of simple Celery app:
```python
from celery import Celery

app = Celery('tasks', broker='pyamqp://guest@localhost//')

@app.task
def add(x, y):
    return x + y
```

### Run Celery worker server 
```shell
celery -A tasks worker --loglevel=INFO
```

### In the Python console run the async task
```python
from tasks import add
result = add.delay(5, 8)
# getting the result with a timeout
result.get(timeout=1)
# getting the result without an exception
result.get(propagate=False)
# getting the traceback of async task
result.traceback
```

## Configure Celery in the Django project
> https://docs.celeryproject.org/en/stable/django/first-steps-with-django.html

## Create celery directory in the project
* Create main celery app directory, for example name it worker
* Create app.py file for creating celery app. Example:
```python
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
    broker_url = None  # pragma: no cover

app = Celery('worker')

app.conf.broker_url = broker_url

app.conf.result_backend = REDIS_RESULTS_BACKEND

app.config_from_object(config)
# it's possible to use configs from django default settings module with namespace:
# app.config_from_object('django.conf:settings', namespace='CELERY')


app.autodiscover_tasks(['worker'])

```
* Import celery app in __init__.py in the celery app directory:
```python
from .app import app as celery_app
```
* Create directory worker/email for example to add the tasks.py file with the tasks 
and empty init file. For example tasks.py file may contain:
```python
from worker.app import app

@app.task
def task_addition(a, b):
    print(f'task_addition: {a + b}')
    return a + b
```

## Configure .env file
* add Celery configs to .env file (don't forget to add this vars to python, django consoles
and to the terminal env vars:
```shell
RABBITMQ_HOST=127.0.0.1
RABBITMQ_PORT=5674
RABBITMQ_DEFAULT_USER=admin
RABBITMQ_DEFAULT_PASS=adminsecret
RABBITMQ_DEFAULT_VHOST=celery
```

## use celery task in the python file
```python
from worker.email.tasks import task_addition


task_addition.delay(2, 2)
```

## Run docker container with celery management
```shell
docker run -d \        
--name brigadier-rmq --hostname brigadier-rmq \
-p 15674:15672 -p 5674:5672 \
rabbitmq:3.8.14-management-alpine
```

### Redis result backend

## Install redis
```shell
pip install redis
```

## Pull docker container and run it. Example:
```shell
docker pull redis:6.2.5-alpine
docker run --name brigadier-redis -p 6379 -d redis:6.2.5-alpine
```

## Add result backend in app.py:
```python
...
REDIS_RESULTS_BACKEND = env.get('REDIS_RESULTS_BACKEND')
...
app.conf.result_backend = REDIS_RESULTS_BACKEND
...
```

## Add env var to env file:
```text
REDIS_RESULTS_BACKEND=redis://localhost:6379/0
```

## Run celery app
```shell
celery -A worker.app worker
```

## Look at the results of completed task:
```shell
telnet localhost 6379
# Press '^]'. Get all keys of results:
>>> KEYS *
# Get the value of result by key:
>>> GET key
```

## profit