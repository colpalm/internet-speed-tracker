# Build Stage
FROM python:3.12-slim AS builder

# Set working directory
WORKDIR /app

COPY backend/pyproject.toml backend/poetry.lock ./

RUN pip install poetry && \
    poetry self add poetry-plugin-export

# Export dependencies to requirements.txt for installation during Runtime Stage
RUN poetry export -f requirements.txt --without-hashes --only main,speedtest -o requirements.txt

# Runtime Stage
FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Install LibreSpeed CLI
RUN apt-get update && apt-get install -y \
    curl \
    unzip \
    wget \
    && wget https://github.com/librespeed/speedtest-cli/releases/latest/download/librespeed-cli_1.0.11_linux_arm64.tar.gz \
    && tar -xzf librespeed-cli_1.0.11_linux_arm64.tar.gz -C /usr/local/bin/ \
    && chmod +x /usr/local/bin/librespeed-cli \
    && rm librespeed-cli_1.0.11_linux_arm64.tar.gz \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file from builder
COPY --from=builder /app/requirements.txt .

# Install runtime dependencies and add user
RUN pip install --no-cache-dir -r requirements.txt && \
    adduser --disabled-password --gecos "" appuser

# Copy application code
COPY backend/speedtest ./speedtest
COPY backend/shared ./shared

# Copy the entrypoint script
COPY docker/speedtest/entrypoint.sh ./

# Set permissions
RUN chmod +x ./entrypoint.sh && \
    chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

ENTRYPOINT ["./entrypoint.sh"]