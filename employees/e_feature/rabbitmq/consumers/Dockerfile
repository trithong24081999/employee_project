# backend/employees/e-feature/rabbitmq/consumers/Dockerfile

FROM python:3.10-slim

WORKDIR /app
COPY . /app

RUN pip install --upgrade pip

RUN pip install -r /app/backend/employees/e_feature/rabbitmq/consumers/requirements.txt

