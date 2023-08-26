FROM python:3.11

WORKDIR /channelsdb

COPY requirements.txt /channelsdb/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /channelsdb/requirements.txt

RUN mkdir /data

COPY config_docker.ini /channelsdb/config.ini

COPY src/api /channelsdb/code/api

COPY assets /channelsdb/assets

WORKDIR /channelsdb/code

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "80"]
