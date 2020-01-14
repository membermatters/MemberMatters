#!/bin/sh
# Start nginx
service nginx start

# Navigate to the app and start gunicorn
cd memberportal
exec gunicorn memberportal.wsgi:application --bind unix:/tmp/gunicorn.sock --access-logfile '/usr/src/logs/access.log' --error-logfile '/usr/src/logs/error.log' --workers 6