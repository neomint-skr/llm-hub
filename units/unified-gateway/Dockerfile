# Multi-stage build for Unified Gateway
# Stage 1: Builder
FROM python:3.11-alpine AS builder

# Install build dependencies
RUN apk add --no-cache \
    gcc \
    musl-dev \
    libffi-dev

# Create app user for build
RUN adduser -D -s /bin/sh appuser

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY units/unified-gateway/requirements.txt .

# Install Python dependencies to user directory
RUN pip install --user --no-cache-dir -r requirements.txt

# Copy application code and platform
COPY units/unified-gateway/ .
COPY platform/ ./platform/

# Remove build artifacts
RUN find /root/.local -name "*.pyc" -delete && \
    find /root/.local -name "__pycache__" -type d -exec rm -rf {} + || true

# Stage 2: Final runtime image
FROM python:3.11-alpine AS final

# Install runtime dependencies only
RUN apk add --no-cache \
    wget \
    && rm -rf /var/cache/apk/*

# Create non-root user
RUN adduser -D -s /bin/sh -u 1000 appuser

# Set working directory
WORKDIR /app

# Copy Python packages from builder
COPY --from=builder /root/.local /home/appuser/.local

# Copy application code and platform
COPY --chown=appuser:appuser units/unified-gateway/ .
COPY --chown=appuser:appuser platform/ ./platform/

# Add platform directory to Python path
ENV PYTHONPATH="/app:/app/platform:${PYTHONPATH}"

# Set user's local bin in PATH
ENV PATH="/home/appuser/.local/bin:${PATH}"

# Switch to non-root user
USER 1000:1000

# Expose Gateway port
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD wget -q --spider http://localhost:8080/health || exit 1

# Default command
CMD ["./start.sh"]
