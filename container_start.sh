#!/bin/sh
# Start nginx
service nginx start

# Navigate to the app and start gunicorn
cd memberportal

# We should migrate on startup in case there's been any db changes
python manage.py migrate

if [ ! -f /usr/src/data/setupcomplete ]; then
    echo "WARNING: Setup has not completed. Populating database with defaults."
    python manage.py loaddata initial
    touch /usr/src/data/setupcomplete
fi

exec gunicorn membermatters.wsgi:application --bind unix:/tmp/gunicorn.sock --access-logfile '/usr/src/logs/access.log' --error-logfile '/usr/src/logs/error.log' --workers 6
