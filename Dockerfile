# Specify our base image
FROM nikolaik/python-nodejs:python3.8-nodejs12
MAINTAINER Jaimyn Mayer (infrastructure@hsbne.org)

# Install nginx
RUN apt-get update && apt-get install -y nginx

# Copy our requirements across and install dependencies
# Splitting this and copying the full code means we take advantage of the docker cache layers and don't have to
# reinstall everything when the code changes
RUN mkdir /usr/src/app && mkdir /usr/src/logs && mkdir /usr/src/data
ADD ./requirements.txt /usr/src/app
WORKDIR /usr/src/app
RUN pip install --no-cache-dir -r requirements.txt

# Copy over the nginx config file
ADD ./nginx.conf /etc/nginx/nginx.conf

# Add the rest of our code and build it
ADD . /usr/src/app

WORKDIR /usr/src/app/memberportal/
RUN python manage.py collectstatic --noinput

WORKDIR /usr/src/app/frontend
RUN npm install
RUN npm run build

# We don't want people to access our .npmrc config after we publish this image!
RUN rm -f .npmrc

VOLUME /usr/src/data
VOLUME /usr/src/logs
WORKDIR /usr/src/app

# Expose the port and run the app
EXPOSE 8000
CMD ["sh", "/usr/src/app/container_start.sh"]
