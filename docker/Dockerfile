# Specify our base image
FROM alpine:3.14
LABEL maintainer="Jaimyn Mayer (github@jaimyn.com.au)"
LABEL description="Base Dockerfile for the MemberMatters software."

VOLUME /usr/src/data/
VOLUME /usr/src/logs/

# Copy over the nginx config file
ADD docker/nginx.conf /etc/nginx/nginx.conf
ADD . /usr/src/app/
WORKDIR /usr/src/app/

# Install nginx and other build dependencies
RUN apk update \
    && apk add make gcc g++ musl-dev libffi-dev openssl-dev zlib-dev jpeg-dev bash libpng-dev openrc cargo nginx vips-dev python2 python3 python3-dev py3-pip mariadb-dev nodejs npm  \
    # Create some base folders for everything
    && mkdir -p /usr/src/app/frontend && mkdir /usr/src/logs && mkdir /usr/src/data \

    # Install node deps
    && cd /usr/src/app/frontend/ \
    && npm ci \

    # Install python deps
    && cd /usr/src/app/memberportal/ \
    $$ pip3 install --no-cache-dir pillow \
    && pip3 install --no-cache-dir -r requirements.txt \ 
    && python3 manage.py collectstatic --noinput \

    # Build our frontend
    && cd /usr/src/app/frontend/ \
    && npm run build \

    # Remove node_modules and our .npmrc
    && rm -rf .npmrc node_modules/ \

    # Remove build deps we don't need anymore
    && apk del --no-cache --purge make gcc g++ musl-dev libffi-dev openssl-dev zlib-dev jpeg-dev bash libpng-dev cargo vips-dev python2 python3-dev npm \
    && rm -rf /var/cache/apk/* \

    # Expose the port and run the app
    EXPOSE 8000
CMD ["sh", "/usr/src/app/docker/container_start.sh"]
