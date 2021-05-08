# Email, cache, using it for email verification.

## memcached
> https://github.com/memcached/memcached/blob/master/doc/protocol.txt
> https://hub.docker.com/_/memcached?tab=description&page=1&ordering=last_updated
> https://docs.djangoproject.com/en/3.1/topics/cache/#memcached

* Run container with memcached alpine with docker. Port by default -p 11211:11211
```shell
docker run -d -p 11211:11211 --name brigadier-memcached memcached:alpine
```
* telnet
```shell
brew install telnet
```
* Using telnet for managing cache
```shell
telnet localhost 11211
# 0 - is binary format
set A 0 60 4
ilia
get A
set B 0 0 4
ilia
delete B
# stats
stats
stats items
# dump repository with id 1
stats cachedump 1 0
# to exit ctrl + ] and ctrl + D
```
* Using cache in the django console:
```python
from django.core.cache import cache
cache.set('A', 'ilia', timeout=30)
cache.get('A')
```
* Complex cache type:
```python
from django.core.cache import cache
cache.set('hash', {'key':'value', 'key1': 'value1'})
cache.get('hash')
# complex type is encrypted by pickle method
```
* Store sessions into the memcached tutorial:
> https://docs.djangoproject.com/en/3.2/topics/http/sessions/#using-cached-sessions

## smtpd
> https://docs.python.org/3.4/library/smtpd.html
> https://docs.djangoproject.com/en/3.2/topics/email/#smtp-backend

* Create smtpd server
```shell
# with -d - debug
python3 -m smtpd -n -c DebuggingServer -d localhost:1025
```
* Using send_mail in Python:
```python
from django.core.mail import send_mail
send_mail('Hello', 'Hello\nThis is a greeting message\n\nRegards', 'robot@example.com', ['mike@example.com'])
```
* Sending mail with curl
```shell
curl -T - --mail-from from@example.com --mail-rcpt rcpt@example.com \
    smtp://localhost:1025/example.com << _EOF
Subject: This is subject

hi there!
this is my message
done.
_EOF
```
* Running mailcatcher-tool container for administrating emails:
> https://hub.docker.com/r/iliadmitriev/mailcatcher
```shell
docker run -d -p 1080:1080 -p 1025:1025 --name brigadier-mailcatcher iliadmitriev/mailcatcher
```