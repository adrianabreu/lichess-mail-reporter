# The builder image, used to build the virtual environment
FROM python:3.11-buster as builder

ENV VIRTUAL_ENV=/home/packages/.venv
COPY --from=ghcr.io/astral-sh/uv:0.3.3 /uv /bin/uv

ADD . /app
WORKDIR /app

RUN uv sync --frozen

# The runtime image, used to just run the code provided its virtual environment
FROM python:3.11-slim-buster as runtime

WORKDIR /app

ENV VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH" \
    PYTHONPATH="/app" 

COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}
COPY . .