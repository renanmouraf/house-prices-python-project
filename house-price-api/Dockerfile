FROM python:3.8-slim

ENV DEBIAN_FRONTEND noninteractive
ENV TERM linux

WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install python dependencies
COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir --prefer-binary -r /tmp/requirements.txt \
    && find / -name *.pyc -delete

# add app
COPY . .

EXPOSE 8000

CMD "./run_api.sh"