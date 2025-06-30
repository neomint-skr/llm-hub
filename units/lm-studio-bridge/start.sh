#!/bin/sh
# LM Studio Bridge Startup Script
# Validates environment and starts MCP server

set -e

echo "Starting LM Studio Bridge..."

# Validate required environment variables
if [ -z "$LM_STUDIO_URL" ]; then
    echo "ERROR: LM_STUDIO_URL environment variable is required"
    exit 1
fi

# Set default values for optional variables
export MCP_PORT="${MCP_PORT:-3000}"
export LOG_LEVEL="${LOG_LEVEL:-INFO}"
export SERVICE_NAME="${SERVICE_NAME:-lm-studio-bridge}"
export POLL_INTERVAL="${POLL_INTERVAL:-30}"

# Add platform to Python path
export PYTHONPATH="/app:/app/platform:${PYTHONPATH}"

echo "Environment configuration:"
echo "  LM_STUDIO_URL: $LM_STUDIO_URL"
echo "  MCP_PORT: $MCP_PORT"
echo "  LOG_LEVEL: $LOG_LEVEL"
echo "  SERVICE_NAME: $SERVICE_NAME"
echo "  POLL_INTERVAL: $POLL_INTERVAL"

# Handle shutdown signals gracefully
trap 'echo "Received shutdown signal, stopping server..."; kill $PID; wait $PID; exit 0' TERM INT

# Start the MCP server with uvicorn
echo "Starting MCP server on port $MCP_PORT..."
uvicorn api.mcp_server:app \
    --host 0.0.0.0 \
    --port "$MCP_PORT" \
    --log-level info \
    --no-access-log &

PID=$!

# Wait for the server process
wait $PID
