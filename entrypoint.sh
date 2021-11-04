#!/usr/bin/env bash
cd /code
sleep 1m
python manage.py compilemessages
python manage.py collectstatic --noinput
python manage.py runserver 0.0.0.0:8000
