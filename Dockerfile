# The builder image, used to build the virtual environment
FROM ghcr.io/astral-sh/uv:0.4.10-python3.11-bookworm-slim as builder
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy
WORKDIR /app
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project --no-dev

ADD . /app
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev

FROM python:3.11-slim-bookworm

# Copy the application from the builder
COPY --from=builder --chown=app:app /app /app
WORKDIR /app
# Place executables in the environment at the front of the path
ENV PATH="/app/.venv/bin:$PATH"