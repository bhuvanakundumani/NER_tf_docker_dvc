FROM python:3.7-slim

RUN apt update
RUN apt install -y git

ARG AWS_ACCESS_KEY_ID
ARG AWS_SECRET_ACCESS_KEY

ADD requirements.txt /
RUN pip install -r /requirements.txt 

ADD . /app
VOLUME /voldata
WORKDIR /app

RUN dvc remote modify myremote access_key_id ${AWS_ACCESS_KEY_ID}
RUN dvc remote modify myremote secret_access_key ${AWS_SECRET_ACCESS_KEY}
RUN dvc pull

ENV PORT 8088
EXPOSE $PORT

CMD cp -r /app/* /voldata && exec gunicorn --bind :$PORT --workers 1 --threads 8 api:app
