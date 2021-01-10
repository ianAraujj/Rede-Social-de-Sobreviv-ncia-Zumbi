FROM python:3.9
ENV PYTHONUNBUFFERED=1
RUN apt-get update -qq && apt-get install -y wait-for-it
WORKDIR /core
COPY requirements-dev.txt /core/
RUN pip install -r requirements-dev.txt
COPY . /core/