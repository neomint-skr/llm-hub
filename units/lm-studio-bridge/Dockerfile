# Multi-stage build for LM Studio Bridge
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
COPY units/lm-studio-bridge/requirements.txt .

# Install Python dependencies to user directory
RUN pip install --user --no-cache-dir -r requirements.txt

# Copy application code only (no platform to avoid naming conflicts)
COPY units/lm-studio-bridge/ .

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

# Copy application code only (no platform to avoid naming conflicts)
COPY --chown=appuser:appuser units/lm-studio-bridge/ .

# Set user's local bin in PATH
ENV PATH="/home/appuser/.local/bin:${PATH}"

# Switch to non-root user
USER 1000:1000

# Expose MCP port
EXPOSE 3000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD wget -q --spider http://localhost:3000/health || exit 1

# Default command
CMD ["./start.sh"]
