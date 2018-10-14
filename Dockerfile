# Dockerfile for HSBNE member portal.
FROM ubuntu:18.04
MAINTAINER Jaimyn Mayer (infrastructure@hsbne.org)

# Install required packages and remove the apt packages cache when done.
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y \
	python3 \
	python3-dev \
	python3-pip \
	nginx \
	supervisor

# install requirements
ADD requirements.txt /app/requirements.txt
RUN pip3 install -r /app/requirements.txt

# setup all the configfiles
RUN echo "daemon off;" >> /etc/nginx/nginx.conf
ADD nginx-app.conf /etc/nginx/sites-available/default
ADD supervisor-app.conf /etc/supervisor/conf.d/

# add (the rest of) our code
ADD . /app
WORKDIR /app/memberportal

VOLUME /data
RUN python3 manage.py migrate
RUN python3 manage.py loaddata fixtures/initial.json
EXPOSE 8000
CMD ["supervisord", "-n"]
