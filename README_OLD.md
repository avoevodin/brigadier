# Brigadier
[![Python application](https://github.com/avoevodin/brigadier/actions/workflows/python-app.yml/badge.svg)](https://github.com/avoevodin/brigadier/actions/workflows/python-app.yml)
[![codecov](https://codecov.io/gh/avoevodin/brigadier/branch/master/graph/badge.svg?token=FLC8BXMGQN)](https://codecov.io/gh/avoevodin/brigadier)

#### Task manager for handling brigade of the builders.

## Install
* Clone the rep:
```shell
git clone git@github.com:avoevodin/brigadier.git
```
* Create the venv:
```shell
python3 -m venv venv
```
* Activate the venv:
```shell
source venv/bin/activate
```
* Install requirements:
```shell
pip install -r requirements.txt
```
* Open brigadier-project directory
```shell
cd brigadier
```
* Run the memcached container:
```shell
docker run -d -p 11211:11211 --name brigadier-memcached memcached:alpine
```
* Run the smtpd-server. Localhost and port are for example:
```shell
python3 -m smtpd -n -c BrigadierSMTPDServer localhost:1025
```
* Create the .env file. Example:
```shell
cat > .env << __EOF__
POSTGRES_DB=brigadier
POSTGRES_USER=brigadier
POSTGRES_PASSWORD=secret
POSTGRES_HOST=localhost
POSTGRES_PORT=5433
EMAIL_HOST=localhost
EMAIL_PORT=1025
EMAIL_HOST_USER=None
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
RABBITMQ_HOST=127.0.0.1
RABBITMQ_PORT=5674
RABBITMQ_DEFAULT_USER=admin
RABBITMQ_DEFAULT_PASS=adminsecret
RABBITMQ_DEFAULT_VHOST=celery
CACHE_BACKEND=django.core.cache.backends.memcached.MemcachedCache
CACHE_LOCATION=127.0.0.1:11211
REDIS_RESULTS_BACKEND=redis://localhost:6379/0
DJANGO_SETTINGS_MODULE=brigadier.settings
__EOF__
```
* Create and run PostgreSQL docker container:
```shell
docker run -d --name brigadier-postgres --hostname brigadier-postgres \
-p 5433:5432 \
--env-file .env \
postgres:13.2-alpine
```
* Pull the uwsgi-docker image:
```shell
docker pull avo888/brigadier-uwsgi:latest
```
* Create .env-uwsgi file. Example:
```shell
cat > .env-uwsgi << __EOF__
POSTGRES_HOST=brigadier-postgres
POSTGRES_DB=brigadier
POSTGRES_PASSWORD=secret
POSTGRES_PORT=5432
POSTGRES_USER=brigadier
PS1=%n@%m %~ %%
EMAIL_HOST=localhost
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
REDIS_RESULTS_BACKEND=redis://localhost:6379/0
DJANGO_SETTINGS_MODULE=brigadier.settings
__EOF__
```
* Run the uwsgi-docker image:
```shell
docker run -d --name brigadier-uwsgi --hostname brigadier-uwsgi \
-p 8000:8000 \
--env-file brigadier/.env-uwsgi \
--link brigadier-postgres \
avo888/brigadier-uwsgi:latest \
cmd celery -A brigadier worker -l INFO
```
* Create objects from admin console.
    1. Go to the browser and type '127.0.0.1:8000/admin'
    2. Login
    3. Create objects
* Profit

## Develop
* Clone the rep:
```shell
git clone git@github.com:avoevodin/brigadier.git
```
* Create the venv:
```shell
python3 -m venv venv
```
* Activate the venv:
```shell
source venv/bin/activate
```
* Install requirements:
```shell
pip install -r requirements.txt
```
* Run the memcached container:
```shell
docker run -d -p 11211:11211 --name brigadier-memcached memcached:alpine
```
* Run the smtpd-server. -d is a debug-mode:
```shell
python3 -m smtpd -n -c BrigadierSMTPDServer -d localhost:1025
```
* Open brigadier-project directory
```shell
cd brigadier
```
* Create the .env file. Example:
```shell
cat > .env << __EOF__
POSTGRES_DB=brigadier
POSTGRES_USER=brigadier
POSTGRES_PASSWORD=secret
POSTGRES_HOST=localhost
POSTGRES_PORT=5433
EMAIL_HOST=localhost
EMAIL_PORT=1025
EMAIL_HOST_USER=None
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
RABBITMQ_HOST=127.0.0.1
RABBITMQ_PORT=5674
RABBITMQ_DEFAULT_USER=admin
RABBITMQ_DEFAULT_PASS=adminsecret
RABBITMQ_DEFAULT_VHOST=celery
CACHE_BACKEND=django.core.cache.backends.memcached.MemcachedCache
CACHE_LOCATION=127.0.0.1:11211
REDIS_RESULTS_BACKEND=redis://localhost:6379/0
DJANGO_SETTINGS_MODULE=brigadier.settings
__EOF__
```
* Create and run PostgreSQL docker container:
```shell
docker run -d --name brigadier-postgres --hostname brigadier-postgres \
-p 5433:5432 \
--env-file .env \
postgres:13.2-alpine
```

### Run server from the terminal
* Export env vars from env-file:
```shell
export $(cat .env)
```
* Compile messages:
```shell
cd brigadier
./manage.py compilemessages
```
* Migrate:
```shell
./manage.py migrate --no-input
```
* Collect static:
```shell
python3 manage.py collectstatic --no-input
```
* Create superuser:
```shell
./manage.py createsuperuser
```
* Configure server
    1. Create django-server configuration.
    2. Point paths to django-project and its settings.
    3. In mysite/settings.py configure ALLOWED_HOSTS with '*',
        if it hasn't been done before.
* Run server from the terminal:
```shell
./manage.py runserver 0:8000
```
* Create objects from admin console.
    1. Go to the browser and type '127.0.0.1:8000/admin'
    2. Login
    3. Create objects

### Run server from the docker container with uwsgi:
* Settings for uwsgi in uwsgi.ini:
```ini
[uwsgi]
http-socket=0.0.0.0:8000
chdir=%d
workers=%k
threads=%k
module=brigadier.wsgi:application
master=True

;pidfile=%duwsgi-master.pid
;daemonize=%duwsgi.log

env DJANGO_DEBUG=False
env DJANGO_SETTINGS_MODULE=brigadier.settings

plugins = python3,http

offload-threads = %k
static-map=/static=%dstatic
check-static=%dstatic
static-expires=%dstatic/* 86400
```
* Create the requirements_docker.txt file, if it doesn't exist:
```shell
cat requirements_docker.txt << __EOF__
asgiref==3.3.1
coverage==5.5
Django==3.1.7
pytz==2021.1
sqlparse==0.4.1
__EOF__
```
* Dockerfile:
```dockerfile
FROM alpine:3.13

RUN apk add python3 py3-pip py3-psycopg2 uwsgi uwsgi-python3 uwsgi-http gettext

COPY requirements_docker.txt /app/requirements.txt

RUN pip install -r /app/requirements.txt

COPY brigadier/ /app/brigadier/
WORKDIR /app/brigadier/

RUN python3 manage.py collectstatic --no-input
RUN python3 manage.py compilemessages

CMD uwsgi --ini uwsgi.ini

```
* Create the docker-image from the Dockerfile:
```shell
docker build -f Dockerfile -t brigadier-uwsgi ./
```
* Create .env-uwsgi file. Example:
```shell
cat > .env-uwsgi << __EOF__
POSTGRES_HOST=brigadier-postgres
POSTGRES_DB=brigadier
POSTGRES_PASSWORD=secret
POSTGRES_PORT=5432
POSTGRES_USER=brigadier
PS1=%n@%m %~ %%
EMAIL_HOST=localhost
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
REDIS_RESULTS_BACKEND=redis://localhost:6379/0
DJANGO_SETTINGS_MODULE=brigadier.settings
__EOF__
```
* Run container based on the created docker-image:
```shell
docker run --name brigadier-uwsgi --hostname brigadier-uwsgi \
-d -p 8000:8000 --env-file .env-uwsgi --link brigadier-postgres \
brigadier-uwsgi \
cmd celery -A brigadier worker -l INFO
```
* Push repository to the docker hub:
```shell
docker push avo888/brigadier-uwsgi:latest
```
* Making data migrations:
  1. Create empty migration (it's good to use the name of the migration):
  ```shell
  python manage.py makemigrations --empty yourappname --name migration_name
  ```
  2. Create migrations code in the added migration file.
  3. To get model you can work from: 
  ```python
  apps.get_model("yourappname", "yourmodelname")
  ```
* Configure [Django Debug Toolbar](DJANGO_ORM_AND_DJANGO_DEBUG_TOOLBAR.md)

## Tests
* Run tests with coverage: 
```shell
coverage run --source='.' manage.py test -v 2
```
* Get report in html of coverage tests:
```shell
coverage html
open htmlcov/index.html
```
