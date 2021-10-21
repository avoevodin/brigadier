# Brigadier
[![Python application](https://github.com/avoevodin/brigadier/actions/workflows/python-app.yml/badge.svg)](https://github.com/avoevodin/brigadier/actions/workflows/python-app.yml)
[![codecov](https://codecov.io/gh/avoevodin/brigadier/branch/master/graph/badge.svg?token=FLC8BXMGQN)](https://codecov.io/gh/avoevodin/brigadier)

This app is the simple and fast project manager which helps you to
save your time and complete projects before deadline.

# Table of contents

- [Brigadier](#brigadier)
  - [Features](#features)
- [Install](#install)
  - [Bare metal install](#bare-metal-install)
    - [Setup services](#setup-services)
    - [Setup environment](#setup-environment)
    - [Run application](#run-application)
    - [Configure](#configure)
  - [Docker install](#docker-install)
    - [Setup docker environment](#setup-docker-environment)
    - [Build image](#build-image)
    - [Migrate](#migrate)
    - [Run docker containers](#run-docker-containers)
    - [Create superuser](#create-superuser)
  - [Development](#development)
    - [Bare metal install and setup services](#bare-metal-install-and-setup-services)
    - [Setup environment with an active django debug](#setup-environment-with-an-active-django-debug)
    - [Run application](#run-application)
  - [Testing](#testing)
    - [Test project](#test-project)
    - [Test project with verbosity](#test-project-with-verbosity)
    - [Run coverage with verbosity 2](#run-coverage-with-verbosity-2)
    - [Look at the coverage report](#look-at-the-coverage-report)
    - [Look at the coverage html report](#look-at-the-coverage-html-report)
    - [Create the coverage xml report](#create-the-coverage-xml-report)
    - [Check if coverage under 100](#check-if-coverage-under-100)

## Features
* Task manager
* Project manager
* Employee manager
* Overdue, complete, processed tasks and projects monitor
* Occupied employees, employees with overdue tasks and without any task monitor

# Install

Clone the rep:
```shell
git clone git@github.com:avoevodin/brigadier.git
cd brigadier
```

## Bare metal install

1. Create the venv:
```shell
python3 -m venv venv
```
2. Activate the venv:
```shell
source venv/bin/activate
```
3. Install requirements:
```shell
pip install -r requirements.txt
```

### Setup services

1. Postgres
```shell
# create .env-postgres file with initial db options
cat > .env-postgres <<_EOF
POSTGRES_DB=brigadier
POSTGRES_USER=brigadier
POSTGRES_PASSWORD=secret
_EOF

# create docker instance
docker run -d --name brigadier-postgres \
        --hostname brigadier-postgres \
        -p 5432:5432 --env-file .env-postgres \
        postgres:14-alpine
```
2. RabbitMQ
```shell
# create .env-rmq file with initial rmq options
cat > .env-rmq <<_EOF
RABBITMQ_DEFAULT_USER=admin
RABBITMQ_DEFAULT_PASS=adminsecret
RABBITMQ_DEFAULT_VHOST=celery
_EOF

# create docker instance
docker run -d --name brigadier-rmq \
        --hostname brigadier-rmq \
        -p 5672:5672 -p 15672:15672 \
        --env-file .env-rmq \
        rabbitmq:3.8.14-management-alpine
```
3. Memcached
```shell
# create docker instance
docker run -d --name brigadier-memcached \
        --hostname brigadier-memcached \
        -p 11211:11211 \
        memcached:alpine
```
4. Redis
```shell
# create docker instance
docker run -d --name brigadier-redis \
        --hostname brigadier-redis \
        -p 6379:6379 \
        redis:6.2.6-alpine
```
5. Mailcatcher(dev only)
```shell
# create docker instance
docker run -d --name brigadier-mailcatcher \
        --hostname brigadier-mailcatcher \
        -p 1025:1025 -p 1080:1080 \
        iliadmitriev/mailcatcher
```

### Setup environment
```shell
# create common .env file for the project
cat > .env <<_EOF
POSTGRES_DB=brigadier
POSTGRES_USER=brigadier
POSTGRES_PASSWORD=secret
POSTGRES_HOST=127.0.0.1
POSTGRES_PORT=5432
EMAIL_HOST=127.0.0.1
EMAIL_PORT=1025
EMAIL_HOST_USER=None
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
RABBITMQ_HOST=127.0.0.1
RABBITMQ_PORT=5672
RABBITMQ_DEFAULT_USER=admin
RABBITMQ_DEFAULT_PASS=adminsecret
RABBITMQ_DEFAULT_VHOST=celery
CACHE_BACKEND=django.core.cache.backends.memcached.MemcachedCache
CACHE_LOCATION=127.0.0.1:11211
REDIS_RESULTS_BACKEND=redis://127.0.0.1:6379/0
DJANGO_SETTINGS_MODULE=brigadier.settings
DJANGO_DEBUG=False
_EOF

# export env vars
export $(cat .env)
```

### Run application
* Apply migrations
```shell
cd brigadier
python3 manage.py migrate --no-input
```
* Compile messages
```shell
# notice that you must be in the brigadier/brigadier directory
python3 manage.py compilemessages
```
* Collect static
```shell
# notice that you must be in the brigadier/brigadier directory
python3 manage.py collectstatic --no-input
```
* Run uwsgi server
```shell
uwsgi --ini uwsgi.ini
```
* Run celery worker
```shell
# notice that you must be in the brigadier/brigadier directory,
# python venv must be activated, env vars must be exported.
celery -A worker.app worker
```
* Run celery beat
```shell
# notice that you must be in the brigadier/brigadier directory,
# python venv must be activated, env vars must be exported.
celery -A worker.app beat 
```

### Configure
```shell
# create super user.
# Notice that you must be in the brigadier/brigadier directory,
# python venv must be activated, env vars must be exported.
python3 manage.py createsuperuser
```

## Docker install

[Setup services](#setup-services)

### Setup docker environment
```shell
# create common .env file for the project. IP address just for example,
# find out your current address before configuring.
cat > .env <<_EOF
POSTGRES_DB=brigadier
POSTGRES_USER=brigadier
POSTGRES_PASSWORD=secret
POSTGRES_HOST=192.168.1.46
POSTGRES_PORT=5432
EMAIL_HOST=192.168.1.46
EMAIL_PORT=1025
EMAIL_HOST_USER=None
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
RABBITMQ_HOST=192.168.1.46
RABBITMQ_PORT=5672
RABBITMQ_DEFAULT_USER=admin
RABBITMQ_DEFAULT_PASS=adminsecret
RABBITMQ_DEFAULT_VHOST=celery
CACHE_BACKEND=django.core.cache.backends.memcached.MemcachedCache
CACHE_LOCATION=192.168.1.46:11211
REDIS_RESULTS_BACKEND=redis://192.168.1.46:6379/0
DJANGO_SETTINGS_MODULE=brigadier.settings
DJANGO_DEBUG=False
_EOF
```

### Build image
```shell
docker build -f Dockerfile -t brigadier-django ./
```

### Migrate
```shell
docker run --name brigadier-migrations \
        --hostname brigadier-migrations \
        --rm -ti --env-file .env \
        brigadier-django \
        python3 manage.py migrate --no-input
```

### Run docker containers
* Run uwsgi container:
```shell
docker run --name brigadier-uwsgi \
        --hostname brigadier-uwsgi \
        -d -p 8000:8000 --env-file .env \
        brigadier-django
```
* Run celery container:
```shell
docker run --name brigadier-celery \
        --hostname brigadier-celery \
        -d --env-file .env \
        brigadier-django \
        celery -A worker.app worker
```
* Run celery beat container:
```shell
docker run --name brigadier-celery-beat \
        --hostname brigadier-celery-beat \
        -d --env-file .env \
        brigadier-django \
        celery -A worker.app beat
```

### Create superuser
```shell
docker run --name brigadier-createsuperuser \
        --hostname brigadier-createsuperuser \
        --rm -ti --env-file .env \
        brigadier-django \
        python3 manage.py createsuperuser
```

## Development

### Bare metal install and setup services

1. [Bare metal install](#bare-metal-install)

2. [Setup services](#setup-services)

### Setup environment with an active django debug
```shell
# create common .env file for the project
cat > .env <<_EOF
POSTGRES_DB=brigadier
POSTGRES_USER=brigadier
POSTGRES_PASSWORD=secret
POSTGRES_HOST=127.0.0.1
POSTGRES_PORT=5432
EMAIL_HOST=127.0.0.1
EMAIL_PORT=1025
EMAIL_HOST_USER=None
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
RABBITMQ_HOST=127.0.0.1
RABBITMQ_PORT=5672
RABBITMQ_DEFAULT_USER=admin
RABBITMQ_DEFAULT_PASS=adminsecret
RABBITMQ_DEFAULT_VHOST=celery
CACHE_BACKEND=django.core.cache.backends.memcached.MemcachedCache
CACHE_LOCATION=127.0.0.1:11211
REDIS_RESULTS_BACKEND=redis://127.0.0.1:6379/0
DJANGO_SETTINGS_MODULE=brigadier.settings
DJANGO_DEBUG=True
_EOF

# export env vars
export $(cat .env)
```

### Run application
* Apply migrations
```shell
cd brigadier
python3 manage.py migrate --no-input
```
* Make and compile locale messages
```shell
# notice that you must be in the brigadier/brigadier directory
python3 manage.py makemessages -l en
python3 manage.py makemessages -l ru
python3 manage.py compilemessages
```
* Collect static
```shell
python3 manage.py collectstatic --no-input
```
* Run server
```shell
python3 manage.py runserver 0:8000
```
* Run celery worker
```shell
# notice that you must be in the brigadier/brigadier directory,
# python venv must be activated, env vars must be exported.
celery -A worker.app worker
```
* Run celery beat
```shell
# notice that you must be in the brigadier/brigadier directory,
# python venv must be activated, env vars must be exported.
celery -A worker.app beat 
```

* Configure [Django Debug Toolbar](DJANGO_ORM_AND_DJANGO_DEBUG_TOOLBAR.md)

## Testing

1. [Bare metal install](#bare-metal-install)

### Test project
```shell
# notice that you must be in the brigadier/brigadier directory,
# python venv must be activated, env vars must be exported.
python3 manage.py test
```
### Test project with verbosity
```shell
# notice that you must be in the brigadier/brigadier directory,
python3 manage.py test -v 2
```
### Run coverage with verbosity 2
```shell
# notice that you must be in the brigadier/brigadier directory,
coverage run --source='.' manage.py test --verbosity=2
```
### Look at the coverage report
```shell
# notice that you must be in the brigadier/brigadier directory,
coverage report -m
```
### Look at the coverage html report
```shell
# notice that you must be in the brigadier/brigadier directory,
coverage html
open htmlcov/index.html
```
### Create the coverage xml report
```shell
# notice that you must be in the brigadier/brigadier directory,
coverage xml
```
### Check if coverage under 100
```shell
coverage report --fail-under=100
```

* Profit