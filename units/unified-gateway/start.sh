#!/bin/sh
# Unified Gateway Startup Script
# Validates environment and starts Gateway server

set -e

echo "Starting Unified Gateway..."

# Validate required environment variables
if [ -z "$API_KEY" ]; then
    echo "ERROR: API_KEY environment variable is required"
    echo "Please set API_KEY to secure your gateway"
    echo "Example: API_KEY=your-secure-api-key"
    exit 1
fi

if [ -z "$BRIDGE_URL" ]; then
    echo "ERROR: BRIDGE_URL environment variable is required"
    echo "Please set BRIDGE_URL to your bridge service endpoint"
    echo "Example: BRIDGE_URL=http://lm-studio-bridge:3000"
    exit 1
fi

# Set default values for optional variables
export GATEWAY_PORT="${GATEWAY_PORT:-8080}"
export LOG_LEVEL="${LOG_LEVEL:-INFO}"
export SERVICE_NAME="${SERVICE_NAME:-unified-gateway}"
export AUTH_ENABLED="${AUTH_ENABLED:-true}"
export RATE_LIMIT_PER_MINUTE="${RATE_LIMIT_PER_MINUTE:-60}"

# Add platform to Python path
export PYTHONPATH="/app:/app/platform:${PYTHONPATH}"

echo "Environment configuration:"
echo "  BRIDGE_URL: $BRIDGE_URL"
echo "  GATEWAY_PORT: $GATEWAY_PORT"
echo "  LOG_LEVEL: $LOG_LEVEL"
echo "  SERVICE_NAME: $SERVICE_NAME"
echo "  AUTH_ENABLED: $AUTH_ENABLED"
echo "  RATE_LIMIT_PER_MINUTE: $RATE_LIMIT_PER_MINUTE"

# Validate Python environment
if ! python -c "import sys; print(f'Python {sys.version}')" 2>/dev/null; then
    echo "ERROR: Python runtime not available"
    exit 1
fi

# Wait for Bridge service health (max 60s)
echo "Waiting for Bridge service health..."
WAIT_COUNT=0
MAX_WAIT=12  # 12 * 5 = 60 seconds

while [ $WAIT_COUNT -lt $MAX_WAIT ]; do
    if python -c "
import urllib.request
try:
    urllib.request.urlopen('$BRIDGE_URL/health', timeout=5)
    exit(0)
except:
    exit(1)
" >/dev/null 2>&1; then
        echo "✓ Bridge service is healthy"
        break
    fi

    WAIT_COUNT=$((WAIT_COUNT + 1))
    echo "  Waiting for bridge... ($WAIT_COUNT/$MAX_WAIT)"
    sleep 5
done

if [ $WAIT_COUNT -eq $MAX_WAIT ]; then
    echo "WARNING: Bridge service not responding at $BRIDGE_URL"
    echo "Gateway will start but may not function properly"
fi

# Enhanced graceful shutdown handler
shutdown_handler() {
    echo "🛑 Received shutdown signal, initiating graceful shutdown..."

    # Set shutdown timeout
    SHUTDOWN_TIMEOUT=${GRACEFUL_SHUTDOWN_TIMEOUT:-25}
    echo "⏱️  Shutdown timeout: ${SHUTDOWN_TIMEOUT}s"

    # Signal the Python process to shutdown gracefully
    if [ -n "$PID" ] && kill -0 "$PID" 2>/dev/null; then
        echo "📤 Sending SIGTERM to gateway process (PID: $PID)..."
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
        rm -f "$SHARED_STATE_DIR/gateway.ready" 2>/dev/null || true
        echo "gateway_shutdown=$(date -Iseconds)" > "$SHARED_STATE_DIR/gateway.shutdown" 2>/dev/null || true
    fi

    echo "🏁 Unified Gateway shutdown complete"
    exit 0
}

# Set up signal handlers
trap 'shutdown_handler' TERM INT

# Start the Gateway server with enhanced graceful shutdown support
echo "🚀 Starting Unified Gateway with graceful shutdown support..."

# Create enhanced startup script
python -c "
import sys
import signal
import os
from pathlib import Path
sys.path.insert(0, str(Path('/app')))

print('🚀 Starting Unified Gateway with graceful shutdown support...')

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
    import uvicorn
    from uvicorn import Config, Server
    from api.gateway_server import app

    # Create server configuration
    config = Config(
        app=app,
        host='0.0.0.0',
        port=int('$GATEWAY_PORT'),
        log_level='warning',
        access_log=False,
        loop='asyncio'
    )

    # Create server instance
    server_instance = Server(config)

    print(f'✅ Unified Gateway ready on port $GATEWAY_PORT')
    print('🔄 Server starting...')

    # Run server with graceful shutdown support
    server_instance.run()

    print('🏁 Server stopped gracefully')

except KeyboardInterrupt:
    print('⌨️  Keyboard interrupt received')
except Exception as e:
    print(f'❌ ERROR: Gateway startup failed: {e}')
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

echo "🏁 Unified Gateway process completed"
