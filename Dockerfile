# Specify our base image
FROM nikolaik/python-nodejs:python3.8-nodejs12-alpine
MAINTAINER Jaimyn Mayer (github@jaimyn.com.au)

# Install nginx and other build dependencies
RUN apk update && apk add --no-cache nginx make gcc g++ musl-dev libffi-dev openssl-dev zlib-dev jpeg-dev openrc

# Create some base folders for everything
RUN mkdir /usr/src/app && mkdir /usr/src/logs && mkdir /usr/src/data

# Copy our requirements across and install dependencies
# Splitting this and copying the full code means we take advantage of the docker cache layers and don't have to
# reinstall everything when the code changes
ADD memberportal/requirements.txt /usr/src/app
WORKDIR /usr/src/app
RUN pip install --no-cache-dir -r requirements.txt

# Copy over the nginx config file
ADD docker/nginx.conf /etc/nginx/nginx.conf

# Add the rest of our code and build it
ADD . /usr/src/app

WORKDIR /usr/src/app/memberportal/
RUN python manage.py collectstatic --noinput

WORKDIR /usr/src/app/frontend
RUN npm ci && npm run build

# Remove node_modules and our .npmrc
RUN rm -rf .npmrc node_modules

VOLUME /usr/src/data
VOLUME /usr/src/logs
WORKDIR /usr/src/app

# Expose the port and run the app
EXPOSE 8000
CMD ["sh", "/usr/src/app/docker/container_start.sh"]
