# ----------- Stage 1: Builder -----------------
FROM python:3.13 AS builder

ENV DJANGO_SETTINGS_MODULE=config.settings
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

# Install ffmpeg and Poetry for build stage
RUN apt-get update && \
    pip install poetry && \
    rm -rf /var/lib/apt/lists/*

# Install dependencies
COPY poetry.lock pyproject.toml ./
RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi --no-root

# ----------- Stage 2: Final image -------------
FROM python:3.13-slim

ENV DJANGO_SETTINGS_MODULE=config.settings
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install ffmpeg again (we need it at runtime)
RUN apt-get update && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy only the installed packages and bin from builder
COPY --from=builder /usr/local/lib/python3.13 /usr/local/lib/python3.13
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy actual app code (excluding media/static if you're mounting)
COPY . .

