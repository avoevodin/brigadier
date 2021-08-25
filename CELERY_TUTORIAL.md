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
* Create app.py file for creating celery app:
```python
from celery import Celery


app = Celery('worker')

app.conf.broker_url = 'pyamqp://guest:guest@127.0.0.1:5672/celery'

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
## Run celery app
```shell
celery -A worker.app worker
```

## profit