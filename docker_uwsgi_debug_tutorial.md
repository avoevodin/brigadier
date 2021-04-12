* Algorithm of daemonizing: 
1. у запущенного процесса (1)  ты делаешь системный вызов на демонизацию
2. далее система делает копию процесса (2)
3. и превращает процесс (2) в демон
4. процессу (1) система вовращает pid процесса (2)
5. процесс (1) записывает pid в файлик
6. процесс (1) заканчивает свою работу

* run uwsgi from container
* export
* check uwsgi.ini
* ping postgres container connection
```shell
ping brigadier-postgres
```
* psql in the container:
```shell
apk add postgresql-client
psql -U $POSTGRES_USER -h $POSTGRES_HOST -p $POSTGRES_PORT -d $POSTGRES_NAME  
>>>d+
```
* try DJANGO_DEBUG=TRUE, set Debug=True in the uwsgi.ini and export var. Run uwsgi:
```shell
export DJANGO_DEBUG=True
```
* inspect docker container:
```shell
docker inspect brigadier-uwsgi
```
* django shell for looking at the DB settings. Use TAB to look at the list of allowed settings.
```shell
python3 manage.py shell
>>>from django.conf import settings
>>>print(settings.DATABASES)
```