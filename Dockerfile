FROM alpine:3.13

RUN apk add python3 py3-pip py3-psycopg2 uwsgi uwsgi-python3 uwsgi-http gettext

COPY requirements_docker.txt /app/requirements.txt

RUN pip install -r /app/requirements.txt

COPY brigadier/ /app/brigadier/
WORKDIR /app/brigadier/

RUN python3 manage.py collectstatic --no-input
RUN python3 manage.py compilemessages

CMD uwsgi --ini uwsgi.ini
CMD celery -A brigadier worker -l INFO
