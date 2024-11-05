# Dockerfile
FROM ruby:3.1-slim
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Install essential packages
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    gh \
    python3-dev \
    libblas-dev \
    liblapack-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set up working directory
WORKDIR /app

# UV docker config reqs per https://docs.astral.sh/uv/guides/integration/docker/
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project

# Installing project separately from dependencies allows optimal layer caching
COPY . /app
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev
ENV PATH="/app/.venv/bin:$PATH"

# Reset the entrypoint, don't invoke `uv`
ENTRYPOINT []

# Install bundler
RUN gem install bundler

# Expose port 4000 for Jekyll
EXPOSE 4000