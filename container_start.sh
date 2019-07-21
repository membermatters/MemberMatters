#!/bin/sh
# Start nginx
service nginx start

# Navigate to the app and start gunicorn
cd memberportal
exec gunicorn memberportal.wsgi:application --bind unix:/tmp/gunicorn.sock --workers 6