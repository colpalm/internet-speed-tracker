# Build Stage
FROM python:3.12-slim AS builder

# Set working directory
WORKDIR /app

COPY backend/pyproject.toml backend/poetry.lock ./

RUN pip install poetry && \
    poetry self add poetry-plugin-export

# Export dependencies to requirements.txt for installation during Runtime Stage
RUN poetry export -f requirements.txt --without-hashes --only main,api,db -o requirements.txt

# Runtime Stage
FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Copy requirements file from builder
COPY --from=builder /app/requirements.txt .

# Install runtime dependencies and add user
RUN pip install --no-cache-dir -r requirements.txt && \
    adduser --disabled-password --gecos "" appuser

# Copy application code
COPY backend/api ./api
COPY backend/database ./database
COPY backend/shared ./shared

# Necessary permissions for user
RUN chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Expose the port
EXPOSE 8000

CMD ["uvicorn", "api.app:app", "--host", "0.0.0.0", "--port", "8000"]