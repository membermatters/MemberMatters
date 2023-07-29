#!/bin/sh

if [ "$MM_RUN_MODE" = "celery_worker" ]
then
  echo CONTAINER MODE: celery worker
  exec celery -A membermatters.celeryapp worker -l INFO
elif [ "$MM_RUN_MODE" = "celery_beat" ]
then
  echo CONTAINER MODE: celery beat
  sleep 10 # wait a few seconds for other services to start
  exec celery -A membermatters.celeryapp beat -l INFO
else
  echo CONTAINER MODE: django webapp
  sleep 5 # wait a few seconds for postgres to start
  # Start nginx
  nginx

  # We should migrate on startup in case there's been any db changes
  python3 manage.py migrate

  exec daphne -b 0.0.0.0 -p 8001 membermatters.asgi:application
fi
