# ChainETL Dockerfile
# Build production-ready image for blockchain data syncing

FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install uv for fast dependency management
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:$PATH"

# Copy project files
COPY pyproject.toml uv.lock ./
COPY src/ ./src/
COPY README.md LICENSE ./

# Install dependencies and create venv
RUN uv sync --frozen --no-dev

# Create non-root user for security
RUN useradd -m -u 1000 chainetl && chown -R chainetl:chainetl /app
USER chainetl

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PATH="/app/.venv/bin:$PATH"

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD chainetl status --chain ethereum || exit 1

# Default command (can be overridden)
ENTRYPOINT ["chainetl"]
CMD ["--help"]
