# make a builder to pull data from
FROM alpine:latest AS builder

RUN apk update && apk --no-cache add unzip python3 python3-dev py3-setuptools py3-pip wget bash py3-virtualenv alpine-sdk

ENV VIRTUAL_ENV=/app
ENV PATH="/app:/app/bin:$PATH"
ENV LANG=C.UTF-8
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY app/ /app
RUN python3 -m venv /app/
WORKDIR /app/

RUN pip3 install --no-cache-dir --upgrade pip && pip3 install --no-cache-dir discord nextcord requests
RUN pwd && wget https://github.com/weddige/pyaiml3/archive/refs/heads/master.zip -O pythonaiml.zip \
  && unzip pythonaiml.zip && cd pyaiml3-master && python3 setup.py install \
  && cd .. && rm pythonaiml.zip && rm -r pyaiml3-master && cd /

RUN ls -R /app/aiml && rm -rf /app/vendor
RUN chmod +x /app/*.py /app/*.sh || exit 0

#FROM python:3-alpine
FROM alpine:latest

COPY --from=builder /app /app
COPY entrypoint.sh /entrypoint.sh
WORKDIR /app

# this is how you activate a venv via docker
ENV VIRTUAL_ENV=/app
ENV PATH="/app:/app/bin:$PATH"
ENV LANG=C.UTF-8
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV BOTINCONTAINER 1
ENV AIML_XML /app/aiml/std-startup.xml
ENV AIML_BRAIN /data/bot.brn

RUN chmod +x /*.sh && apk update && apk --no-cache add python3 py3-virtualenv && rm -rf /usr/lib/python3.9/__pycache__/ \
 && ln -s /app/aiml/* /app/ && find / -name __pycache__ -type d -exec rm -r "{}" \; || echo "running clean"

VOLUME /data

# docker style entrypoints ['cmd'] are broken in podman
ENTRYPOINT /entrypoint.sh
