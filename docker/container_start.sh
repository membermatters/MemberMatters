#!/bin/sh

if [ "$MM_RUN_MODE" = "celery_worker" ]
then
  echo CONTAINER MODE: celery worker
  exec uv run celery -A membermatters.celeryapp worker -l INFO
elif [ "$MM_RUN_MODE" = "celery_beat" ]
then
  echo CONTAINER MODE: celery beat
  exec uv run celery -A membermatters.celeryapp beat -l INFO
else
  echo CONTAINER MODE: django webapp
  # Start nginx
  nginx

  # We should migrate on startup in case there's been any db changes
  uv run manage migrate

  exec uv run daphne -b 0.0.0.0 -p 8001 membermatters.asgi:application
fi
