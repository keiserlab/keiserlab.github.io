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
WORKDIR /setup

# UV docker config reqs per https://docs.astral.sh/uv/guides/integration/docker/
# Set uv proj env since /app/ host-volume mount would hide [default] /app/.venv/
COPY pyproject.toml uv.lock ./
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy
ENV UV_PROJECT_ENVIRONMENT=/opt/venv
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-project
ENV PATH="$UV_PROJECT_ENVIRONMENT/bin:$PATH"

# Reset the entrypoint, don't invoke `uv`
ENTRYPOINT []

# Configure bundler to use named volume path
ENV BUNDLE_PATH=/opt/vendor/bundle
ENV BUNDLE_APP_CONFIG="$BUNDLE_PATH"
COPY Gemfile Gemfile.lock ./

# `bundle update` Gemfile.lock since we're not versioning it
RUN gem install bundler && bundle update --bundler

# Set final workdir for runtime
WORKDIR /app

# Expose port 4000 for Jekyll
EXPOSE 4000