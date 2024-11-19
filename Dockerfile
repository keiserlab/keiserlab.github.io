# Dockerfile
FROM ruby:3.1-slim AS builder
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Install essential packages
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    gh \
    python3-dev \
    libblas-dev \
    liblapack-dev \
    libpq-dev \
    nodejs \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

FROM builder AS dependencies

# Set up working directory
WORKDIR /app

# UV docker config reqs per https://docs.astral.sh/uv/guides/integration/docker/
# Set uv proj env since /app/ host-volume mount would hide [default] /app/.venv/
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy
ENV UV_PROJECT_ENVIRONMENT=/opt/uv/.venv
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project

# Installing project separately from dependencies allows optimal layer caching
COPY . /app
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev
ENV PATH="$UV_PROJECT_ENVIRONMENT/bin:$PATH"

# Reset the entrypoint, don't invoke `uv`
ENTRYPOINT []

FROM dependencies AS uv

# `bundle update` Gemfile.lock since we're not versioning it
COPY Gemfile Gemfile.lock /app/
RUN gem install bundler
RUN bundle update --bundler

FROM uv AS bundler

# Expose port 4000 for Jekyll
EXPOSE 4000