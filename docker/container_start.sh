#!/bin/sh

echo GOT THIS ONE2 "$MM_RUN_MODE"

if [ "$MM_RUN_MODE" = "celery_worker" ]
then
  echo celery worker mode
  exec celery -A membermatters.celeryapp worker -l INFO
elif [ "$MM_RUN_MODE" = "celery_beat" ]
then
  echo celery beat mode
  exec celery -A membermatters.celeryapp beat -l INFO
else
  echo django mode
  # Start nginx
  nginx

  # We should migrate on startup in case there's been any db changes
  python3 manage.py migrate

  if [ ! -f /usr/src/data/setupcomplete ]; then
      echo "INFO: Detected a first time run. Populating the database with defaults."
      python3 manage.py loaddata initial
      touch /usr/src/data/setupcomplete
  fi

  #exec gunicorn membermatters.wsgi:application --bind unix:/tmp/gunicorn.sock --access-logfile '/usr/src/logs/access.log' --error-logfile '/usr/src/logs/error.log' --workers 6
  exec daphne -b 0.0.0.0 -p 8001 membermatters.asgi:application
fi
