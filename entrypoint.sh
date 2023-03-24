#!/bin/sh

sleep 10

python manage.py migrate
python manage.py createcachetable
python manage.py collectstatic  --noinput
gunicorn autosaloon.wsgi:application --bind 0.0.0.0:8000
#python manage.py runserver 0.0.0.0:8000

exec "$@"