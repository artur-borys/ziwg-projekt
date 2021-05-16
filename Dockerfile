# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster
RUN apt update && apt install git -y && python3 -m pip install pipenv
WORKDIR /app
COPY . .
RUN pipenv --python 3.8 && pipenv install --skip-lock
ENTRYPOINT [ "tail", "-f", "/dev/null" ]