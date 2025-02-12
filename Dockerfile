FROM python:3.12-slim AS builder

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY ./src/requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt

# main image
FROM python:3.12-slim

ENV APP_HOME=/app
ENV SESSIONS_FOLDER=/jmsx_sessions

RUN mkdir -p $APP_HOME && mkdir -p $SESSIONS_FOLDER && addgroup --system app && adduser --system --group app
WORKDIR /app

COPY --from=builder $APP_HOME/wheels /wheels
RUN pip install --no-cache /wheels/*
COPY ./src $APP_HOME

RUN chown -R app:app $APP_HOME && chown -R app:app $SESSIONS_FOLDER
USER app
