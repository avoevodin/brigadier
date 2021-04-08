# Brigadier
## Task manager for handling brigade of the builders.

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
* Create the .env file. Example:
```shell
cat > .env << __EOF__
POSTGRES_DB=brigadier
POSTGRES_USER=brigadier
POSTGRES_PASSWORD=secret
POSTGRES_HOST=localhost
POSTGRES_PORT=5433
DJANGO_DEBUG=True
__EOF__
```
* Export env vars from env-file:
```shell
export $(cat .env)
```
* Create and run PostgreSQL docker container:
```shell
docker run -d --name brigadier-postgres --hostname brigadier-postgres \
-p 5433:5432 \
--env-file .env \
postgres:13.2-alpine
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
* Run server:
```shell
./manage.py runserver 0:8000
```
* Create objects from admin console.
    1. Go to the browser and type '127.0.0.1:8000/admin'
    2. Login
    3. Create objects
* Run tests with coverage: 
```shell
coverage run --source='.' manage.py test -v 2
```
* Get report in html of coverage tests:
```shell
coverage html
open htmlcov/index.html
```
* Profit