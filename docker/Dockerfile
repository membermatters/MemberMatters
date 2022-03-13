# Specify our base image
FROM python:3.10-bullseye
LABEL maintainer="Jaimyn Mayer (github@jaimyn.dev)"
LABEL description="Base Dockerfile for the MemberMatters software."

VOLUME /usr/src/data/
VOLUME /usr/src/logs/

RUN mkdir -p /usr/src/app/frontend && mkdir /usr/src/logs && mkdir /usr/src/data

RUN apt-get update -y && apt-get install -y nginx curl daphne

# Install Node
ENV NODE_VERSION=14.15.0
SHELL ["/bin/bash", "--login", "-c"]

RUN curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.35.3/install.sh | bash
RUN nvm install ${NODE_VERSION}
RUN npm config delete prefix
RUN nvm use --delete-prefix v${NODE_VERSION} --silent

# Install node deps
WORKDIR /usr/src/app/frontend/
ADD frontend/package* /usr/src/app/frontend/
RUN npm ci

ADD frontend /usr/src/app/frontend
ADD package.json /usr/src/app/package.json

# Build our frontend
WORKDIR /usr/src/app/frontend/
RUN npm run build

# Remove our .npmrc
RUN rm -rf .npmrc

# Install python deps
WORKDIR /usr/src/app/memberportal/
ADD memberportal/requirements.txt /usr/src/app/memberportal/requirements.txt
RUN python -m pip install --upgrade pip
RUN pip3 install --no-cache-dir pillow
RUN pip3 install --no-cache-dir -r requirements.txt

# collect static files from Django
ADD memberportal /usr/src/app/memberportal
WORKDIR /usr/src/app/memberportal/
RUN python3 manage.py collectstatic --noinput

# Copy over the nginx config and requirement files
ADD docker/nginx.conf /etc/nginx/nginx.conf
ADD docker /usr/src/app/docker

# Expose the port and run the app
EXPOSE 8000
CMD ["sh", "/usr/src/app/docker/container_start.sh"]
