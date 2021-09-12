FROM python:3.8-alpine

LABEL org.opencontainers.image.authors="@Djangoner(Telegram) djangoner6@gmail.com"

RUN COPY . /usr/app
WORKDIR /usr/app

RUN pip install --no-cache-dir requirements.txt


CMD [ "uvicorn", "main:app" ]