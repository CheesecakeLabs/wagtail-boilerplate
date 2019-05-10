FROM python:3.7-alpine

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY requirements.txt .
RUN \
  apk add --no-cache postgresql-libs && \
  apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev && \
  apk add --no-cache jpeg-dev zlib-dev && \
  pip install -r requirements.txt --no-cache-dir && \
  apk --purge del .build-deps

COPY . /usr/src/app
RUN mkdir -p bundles

ENTRYPOINT ["sh", "docker-entrypoint.sh"]
