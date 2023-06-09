FROM python:3.8 AS base

# install redis
RUN apt-get update && apt-get install -y redis-server

# copy the dependencies file to the working directory
COPY requirements.txt /app/requirements.txt
COPY demo /app/demo
COPY post_data.txt /app/post_data.txt

# set working directory
WORKDIR /app

# install dependencies
RUN pip install -r requirements.txt

# set working directory for the Django app
WORKDIR /app/demo

FROM base as django_test
# run the tests
CMD ["python", "manage.py", "test"]

FROM base AS django_app
EXPOSE 8000
CMD "/bin/bash"

FROM base AS celery
# run celery
CMD ["celery", "-A", "demo", "worker", "-l", "info"]
