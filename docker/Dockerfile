# Specify our base image
FROM python:3.12-bullseye
LABEL maintainer="Jaimyn Mayer (github@jaimyn.dev)"
LABEL description="Base Dockerfile for the MemberMatters software."

VOLUME /usr/src/data/
VOLUME /usr/src/logs/

RUN mkdir -p /usr/src/app/frontend /usr/src/logs /usr/src/data

RUN apt-get update -y && apt-get install -y nginx curl

# Install uv
COPY --from=ghcr.io/astral-sh/uv:0.11.8 /uv /uvx /bin/

# Install Node
ENV NODE_VERSION=22.2.0
SHELL ["/bin/bash", "--login", "-c"]

RUN curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.35.3/install.sh | bash
RUN nvm install ${NODE_VERSION}
RUN npm config delete prefix
RUN nvm use --delete-prefix v${NODE_VERSION} --silent

# Install node deps
WORKDIR /usr/src/app/frontend/
COPY src-frontend/package* /usr/src/app/frontend/
RUN npm ci

ADD src-frontend /usr/src/app/frontend
ADD package.json /usr/src/app/package.json

# Install python deps
WORKDIR /usr/src/app/memberportal/
COPY memberportal .
RUN uv sync --locked

# Build our frontend
WORKDIR /usr/src/app/frontend/
RUN npm run build

# Remove our .npmrc
RUN rm -rf .npmrc

# collect static files from Django and add the backend source code
WORKDIR /usr/src/app/memberportal/
RUN uv run manage collectstatic --noinput

# Copy over the nginx config and requirement files
ADD docker/nginx.conf /etc/nginx/nginx.conf
ADD docker /usr/src/app/docker

# Expose the port and run the app
EXPOSE 8000
CMD ["sh", "/usr/src/app/docker/container_start.sh"]
