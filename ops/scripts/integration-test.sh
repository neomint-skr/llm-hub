#!/bin/bash
# Integration Test Script for LLM Hub
# Tests system startup with LM Studio Mock and Health Checks

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
COMPOSE_DIR="$PROJECT_ROOT/ops/compose"

echo "LLM Hub Integration Test"
echo "======================="
echo "Project Root: $PROJECT_ROOT"

# Start Mock LM Studio Server
echo "Starting Mock LM Studio Server..."
python3 "$SCRIPT_DIR/lm-studio-mock.py" &
MOCK_PID=$!
echo "Mock Server PID: $MOCK_PID"

# Wait for Mock Server to start
sleep 3

# Verify Mock Server is running
if ! curl -f http://localhost:1234/v1/models >/dev/null 2>&1; then
    echo "ERROR: Mock LM Studio Server not responding"
    kill $MOCK_PID 2>/dev/null || true
    exit 1
fi
echo "✓ Mock LM Studio Server running"

# Start Docker Compose services
echo "Starting Docker Compose services..."
cd "$COMPOSE_DIR"
docker-compose up -d

# Wait for services to become healthy
echo "Waiting for services to become healthy..."
WAIT_COUNT=0
MAX_WAIT=24  # 24 * 5 = 120 seconds

while [ $WAIT_COUNT -lt $MAX_WAIT ]; do
    BRIDGE_HEALTH=$(docker inspect --format="{{.State.Health.Status}}" lm-studio-bridge 2>/dev/null || echo "unhealthy")
    GATEWAY_HEALTH=$(docker inspect --format="{{.State.Health.Status}}" unified-gateway 2>/dev/null || echo "unhealthy")
    
    if [ "$BRIDGE_HEALTH" = "healthy" ] && [ "$GATEWAY_HEALTH" = "healthy" ]; then
        echo "✓ Both services are healthy"
        break
    fi
    
    WAIT_COUNT=$((WAIT_COUNT + 1))
    echo "  Waiting for health... ($WAIT_COUNT/$MAX_WAIT) Bridge: $BRIDGE_HEALTH, Gateway: $GATEWAY_HEALTH"
    sleep 5
done

if [ $WAIT_COUNT -eq $MAX_WAIT ]; then
    echo "ERROR: Services did not become healthy within timeout"
    docker-compose logs
    docker-compose down
    kill $MOCK_PID 2>/dev/null || true
    exit 1
fi

# Test Service Discovery
echo "Testing Service Discovery..."
echo "Waiting 35 seconds for discovery poll cycle..."
sleep 35

# Check if models appear as MCP tools
echo "Checking MCP tools endpoint..."
TOOLS_RESPONSE=$(curl -s http://localhost:8080/mcp/tools 2>/dev/null || echo "")

if [ -z "$TOOLS_RESPONSE" ]; then
    echo "ERROR: Could not reach MCP tools endpoint"
    docker-compose logs
    docker-compose down
    kill $MOCK_PID 2>/dev/null || true
    exit 1
fi

# Check if we have tools (using basic grep instead of jq)
TOOL_COUNT=$(echo "$TOOLS_RESPONSE" | grep -o '"name"' | wc -l)

if [ "$TOOL_COUNT" -lt 2 ]; then
    echo "ERROR: Expected at least 2 tools, found $TOOL_COUNT"
    echo "Response: $TOOLS_RESPONSE"
    docker-compose down
    kill $MOCK_PID 2>/dev/null || true
    exit 1
fi

echo "✓ Found $TOOL_COUNT MCP tools"

# Verify tool names match models
if echo "$TOOLS_RESPONSE" | grep -q "llama-2-7b-chat" && echo "$TOOLS_RESPONSE" | grep -q "mistral-7b-instruct"; then
    echo "✓ Tool names match mock models"
else
    echo "WARNING: Tool names may not match expected models"
fi

# Test Gateway Health Endpoint
echo "Testing Gateway Health Endpoint..."
HEALTH_RESPONSE=$(curl -s -w "%{http_code}" http://localhost:8080/health 2>/dev/null || echo "000")
HTTP_CODE="${HEALTH_RESPONSE: -3}"
HEALTH_BODY="${HEALTH_RESPONSE%???}"

if [ "$HTTP_CODE" != "200" ]; then
    echo "ERROR: Health endpoint returned HTTP $HTTP_CODE"
    docker-compose down
    kill $MOCK_PID 2>/dev/null || true
    exit 1
fi

echo "✓ Health endpoint returned HTTP 200"

# Check health response content
if echo "$HEALTH_BODY" | grep -q '"status".*"healthy"'; then
    echo "✓ Health status is healthy"
else
    echo "WARNING: Health status may not be healthy"
    echo "Response: $HEALTH_BODY"
fi

# Check for services array
if echo "$HEALTH_BODY" | grep -q '"services"'; then
    echo "✓ Services array present in health response"
else
    echo "WARNING: Services array not found in health response"
fi

# Check for timestamp
if echo "$HEALTH_BODY" | grep -q '"timestamp"'; then
    echo "✓ Timestamp present in health response"
else
    echo "WARNING: Timestamp not found in health response"
fi

echo "✓ Gateway Health test completed successfully"
echo "✓ Service Discovery test completed successfully"
echo "✓ Integration test completed successfully"

# Cleanup
echo "Cleaning up..."
docker-compose down
kill $MOCK_PID 2>/dev/null || true
echo "✓ Cleanup completed"

exit 0
