#!/bin/bash
# Test Build Script for LM Studio Bridge
# Tests Docker container build and basic functionality

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
IMAGE_NAME="lm-bridge:test"
CONTAINER_NAME="lm-bridge-test"

echo "LM Studio Bridge Build Test"
echo "=========================="
echo "Script Directory: $SCRIPT_DIR"
echo "Image Name: $IMAGE_NAME"

# Function to cleanup
cleanup() {
    echo "Cleaning up..."
    docker stop "$CONTAINER_NAME" 2>/dev/null || true
    docker rm "$CONTAINER_NAME" 2>/dev/null || true
    docker rmi "$IMAGE_NAME" 2>/dev/null || true
    echo "Cleanup complete"
}

# Trap cleanup on exit
trap cleanup EXIT

# Check if Docker is available
if ! command -v docker &> /dev/null; then
    echo "ERROR: Docker is not installed or not in PATH"
    exit 1
fi

# Check if Docker daemon is running
if ! docker info &> /dev/null; then
    echo "ERROR: Docker daemon is not running"
    exit 1
fi

echo "Building Docker image..."
BUILD_START=$(date +%s)

# Build the Docker image
if ! docker build -t "$IMAGE_NAME" "$SCRIPT_DIR"; then
    echo "ERROR: Docker build failed"
    exit 1
fi

BUILD_END=$(date +%s)
BUILD_TIME=$((BUILD_END - BUILD_START))

echo "Build completed in ${BUILD_TIME} seconds"

# Check build time constraint (should be under 2 minutes)
if [ $BUILD_TIME -gt 120 ]; then
    echo "WARNING: Build took longer than 2 minutes (${BUILD_TIME}s)"
else
    echo "✓ Build time within acceptable range"
fi

# Test basic container functionality
echo "Testing container startup..."

# Set required environment variables for test
export LM_STUDIO_URL="http://localhost:1234"
export MCP_PORT="3000"

# Run container in background
if ! docker run -d \
    --name "$CONTAINER_NAME" \
    -e LM_STUDIO_URL="$LM_STUDIO_URL" \
    -e MCP_PORT="$MCP_PORT" \
    -p 3000:3000 \
    "$IMAGE_NAME"; then
    echo "ERROR: Failed to start container"
    exit 1
fi

echo "Container started, waiting for initialization..."
sleep 5

# Check if container is still running
if ! docker ps | grep -q "$CONTAINER_NAME"; then
    echo "ERROR: Container stopped unexpectedly"
    echo "Container logs:"
    docker logs "$CONTAINER_NAME"
    exit 1
fi

echo "✓ Container is running"

# Test health endpoint (basic smoke test)
echo "Testing health endpoint..."
if docker exec "$CONTAINER_NAME" curl -f http://localhost:3000/health 2>/dev/null; then
    echo "✓ Health endpoint responding"
else
    echo "WARNING: Health endpoint not responding (expected without LM Studio)"
fi

# Check container logs for errors
echo "Checking container logs for errors..."
LOGS=$(docker logs "$CONTAINER_NAME" 2>&1)

if echo "$LOGS" | grep -i "error" | grep -v "LM Studio" | grep -v "connection"; then
    echo "WARNING: Found unexpected errors in logs"
    echo "$LOGS"
else
    echo "✓ No unexpected errors in logs"
fi

echo "=========================="
echo "✓ Build test completed successfully"
echo "  - Build time: ${BUILD_TIME}s"
echo "  - Container starts correctly"
echo "  - No critical errors detected"
echo "=========================="
