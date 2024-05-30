FROM python:3.11-slim

WORKDIR /channelsdb

RUN --mount=type=bind,source=requirements.txt,target=/channelsdb/requirements.txt,readonly \
    pip install --no-cache-dir --upgrade --root-user-action=ignore -r /channelsdb/requirements.txt

COPY config_docker.ini /channelsdb/config.ini

COPY assets /channelsdb/assets

COPY src/api /channelsdb/code/api

WORKDIR /channelsdb/code

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "80"]
