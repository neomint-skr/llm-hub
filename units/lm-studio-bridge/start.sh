#!/bin/sh
# LM Studio Bridge Startup Script
# Validates environment and starts MCP server

set -e

echo "Starting LM Studio Bridge..."

# Validate required environment variables
if [ -z "$LM_STUDIO_URL" ]; then
    echo "ERROR: LM_STUDIO_URL environment variable is required"
    echo "Please set LM_STUDIO_URL to your LM Studio API endpoint"
    echo "Example: LM_STUDIO_URL=http://host.docker.internal:1234"
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

# Validate Python environment
if ! python -c "import sys; print(f'Python {sys.version}')" 2>/dev/null; then
    echo "ERROR: Python runtime not available"
    exit 1
fi

# Enhanced graceful shutdown handler
shutdown_handler() {
    echo "🛑 Received shutdown signal, initiating graceful shutdown..."

    # Set shutdown timeout
    SHUTDOWN_TIMEOUT=${GRACEFUL_SHUTDOWN_TIMEOUT:-25}
    echo "⏱️  Shutdown timeout: ${SHUTDOWN_TIMEOUT}s"

    # Signal the Python process to shutdown gracefully
    if [ -n "$PID" ] && kill -0 "$PID" 2>/dev/null; then
        echo "📤 Sending SIGTERM to bridge process (PID: $PID)..."
        kill -TERM "$PID" 2>/dev/null

        # Wait for graceful shutdown with timeout
        local elapsed=0
        local interval=1

        while [ $elapsed -lt $SHUTDOWN_TIMEOUT ] && kill -0 "$PID" 2>/dev/null; do
            sleep $interval
            elapsed=$((elapsed + interval))

            if [ $((elapsed % 5)) -eq 0 ]; then
                echo "⏳ Waiting for graceful shutdown... (${elapsed}/${SHUTDOWN_TIMEOUT}s)"
            fi
        done

        # Force kill if still running
        if kill -0 "$PID" 2>/dev/null; then
            echo "⚠️  Graceful shutdown timeout, forcing termination..."
            kill -KILL "$PID" 2>/dev/null
            wait "$PID" 2>/dev/null
            echo "💀 Process forcefully terminated"
        else
            echo "✅ Graceful shutdown completed"
        fi
    else
        echo "⚠️  Process not running or already terminated"
    fi

    # Cleanup shared state
    if [ -n "$SHARED_STATE_DIR" ] && [ -d "$SHARED_STATE_DIR" ]; then
        echo "🧹 Cleaning up shared state..."
        rm -f "$SHARED_STATE_DIR/bridge.ready" 2>/dev/null || true
        echo "bridge_shutdown=$(date -Iseconds)" > "$SHARED_STATE_DIR/bridge.shutdown" 2>/dev/null || true
    fi

    echo "🏁 LM Studio Bridge shutdown complete"
    exit 0
}

# Set up signal handlers
trap 'shutdown_handler' TERM INT

# Start the MCP server with FastMCP
echo "Starting MCP server on port $MCP_PORT..."

# Create enhanced startup script with graceful shutdown support
python -c "
import sys
import signal
import asyncio
import threading
from pathlib import Path
sys.path.insert(0, str(Path('/app')))

print('🚀 Starting LM Studio Bridge with graceful shutdown support...')

# Global shutdown flag
shutdown_requested = False
server_instance = None

def signal_handler(signum, frame):
    global shutdown_requested, server_instance
    print(f'📡 Received signal {signum}, initiating graceful shutdown...')
    shutdown_requested = True

    if server_instance:
        print('🛑 Stopping HTTP server...')
        server_instance.should_exit = True

# Set up signal handlers
signal.signal(signal.SIGTERM, signal_handler)
signal.signal(signal.SIGINT, signal_handler)

try:
    from api.mcp_server import bridge
    import uvicorn
    from uvicorn import Config, Server

    # Initialize the bridge
    print('🔧 Initializing bridge components...')
    bridge.initialize()

    # Get the HTTP app
    app = bridge.get_http_app()

    # Create server configuration
    config = Config(
        app=app,
        host='0.0.0.0',
        port=int('$MCP_PORT'),
        log_level='warning',
        access_log=False,
        loop='asyncio'
    )

    # Create server instance
    server_instance = Server(config)

    print(f'✅ LM Studio Bridge ready on port $MCP_PORT')
    print('🔄 Server starting...')

    # Run server with graceful shutdown support
    server_instance.run()

    print('🏁 Server stopped gracefully')

except KeyboardInterrupt:
    print('⌨️  Keyboard interrupt received')
except Exception as e:
    print(f'❌ ERROR: Bridge startup failed: {e}')
    import traceback
    traceback.print_exc()
    sys.exit(1)
finally:
    print('🧹 Cleanup completed')
" &

PID=$!

# Wait for the server process
echo "⏳ Waiting for server process (PID: $PID)..."
wait $PID

echo "🏁 LM Studio Bridge process completed"
