# Tutorial for debugging of the error with starting uwsgi-docker container.

* Algorithm of daemonizing: 
> 1. System call for daemonize is made for the running process (1).
> 2. System copies process (1) to process (2).
> 3. System turns process (2) to daemon mode.
> 4. System returns pid of the process (2) to the process (1).
> 5. Process (1) write the received pid into the file.
> 6. Process (1) finishes its work.

> That's why daemonize uwsgi inside the docker-container is the wrong way.
> Uwsgi is turned off as a handling process of the container and container
> may be stopped.

* Run uwsgi from container with shell
* Check env vars with export
* Check uwsgi.ini
* Ping postgres container connection from the uwsgi container
```shell
ping brigadier-postgres
```
* Try psql inside the container:
```shell
apk add postgresql-client
psql -U $POSTGRES_USER -h $POSTGRES_HOST -p $POSTGRES_PORT -d $POSTGRES_NAME  
>>>d+
```
* Try DJANGO_DEBUG=TRUE, set Debug=True in the uwsgi.ini or export var. Run uwsgi:
```shell
export DJANGO_DEBUG=True
```
* Inspect docker container:
```shell
docker inspect brigadier-uwsgi
```
* Django shell for looking at the DB settings. Use TAB to look at the list of allowed settings.
```shell
python3 manage.py shell
>>>from django.conf import settings
>>>print(settings.DATABASES)
```