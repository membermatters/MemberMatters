# Specify our base image
FROM python:3.7
MAINTAINER Jaimyn Mayer (infrastructure@hsbne.org)

# Install nginx
RUN apt-get update && apt-get install -y nginx

# Copy our requirements across and install dependencies
# Splitting this and copying the full code means we take advantage of the docker cache layers and don't have to
# reinstall everything when the code changes
RUN mkdir /usr/src/app
ADD ./requirements.txt /usr/src/app
WORKDIR /usr/src/app
RUN pip install --no-cache-dir -r requirements.txt

# Copy over the nginx config file
ADD ./nginx.conf /etc/nginx/nginx.conf

# Add the rest of our code
ADD . /usr/src/app
VOLUME /user/src/app
VOLUME /user/src/envvars

# Expose the port and run the app
EXPOSE 8000
CMD ["sh", "./container_start.sh"]