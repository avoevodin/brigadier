# Tutorial for Celery

## Choose and run the broker
* Run RabbitMQ image from the Docker
```shell
docker run -d --name celery-test-rabbitmq \
--hostname celery-test-rabbitmq -p 5672:5672 rabbitmq 
```

## Install Celery
```shell
pip install celery
```

## Create Celery app
* Example of simple Celery app:
```python
from celery import Celery

app = Celery('tasks', broker='pyamqp://guest@localhost//')

@app.task
def add(x, y):
    return x + y
```

## Run Celery worker server 
```shell
celery -A tasks worker --loglevel=INFO
```

## In the Python console run the async task
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
