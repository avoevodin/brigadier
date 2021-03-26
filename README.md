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
* Run docker container with postgres and download it
if it hasn't been downloaded earlier.
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
./manage.py migrate
```
* Create superuser:
```shell
./manage.py createsuperuser
```
* Run server:
```shell
./manage.py runserver 0:8000
```
* Profit