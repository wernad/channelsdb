FROM python:3.11-slim

ARG APP_NAME=channelsdb

# Update and add basic packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    gcc \
    libc6-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*
 
# Working directory
RUN mkdir -p /opt/${APP_NAME}
WORKDIR /opt/${APP_NAME}

# Dependencies
COPY ["requirements.txt", "/opt/${APP_NAME}"]
RUN --mount=type=bind,source=requirements.txt,target=/${APP_NAME}/requirements.txt,readonly \
    pip install --no-cache-dir --upgrade --root-user-action=ignore -r requirements.txt

# Copy source files.
COPY ["./app", "/opt/${APP_NAME}"]

# Create user
RUN useradd --create-home --shell /bin/bash --user-group ${APP_NAME} \
    && chown -R ${APP_NAME}:${APP_NAME} /opt/${APP_NAME}
USER ${APP_NAME}

# Run app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
