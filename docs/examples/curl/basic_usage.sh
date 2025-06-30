#!/bin/bash
# LLM Hub cURL API Examples
# Basic usage examples for interacting with LLM Hub services using cURL

# Configuration
GATEWAY_URL="http://localhost:8080"
API_KEY="changeme"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}LLM Hub cURL API Examples${NC}"
echo "=========================="
echo "Gateway URL: $GATEWAY_URL"
echo "API Key: ${API_KEY:0:8}..."
echo

# Function to make authenticated requests
make_request() {
    local method="$1"
    local endpoint="$2"
    local data="$3"
    
    if [ "$method" = "GET" ]; then
        curl -s -w "\nHTTP Status: %{http_code}\n" \
             -H "Authorization: Bearer $API_KEY" \
             -H "Content-Type: application/json" \
             "$GATEWAY_URL$endpoint"
    else
        curl -s -w "\nHTTP Status: %{http_code}\n" \
             -X "$method" \
             -H "Authorization: Bearer $API_KEY" \
             -H "Content-Type: application/json" \
             -d "$data" \
             "$GATEWAY_URL$endpoint"
    fi
}

# Function to check if jq is available for JSON formatting
check_jq() {
    if command -v jq &> /dev/null; then
        return 0
    else
        echo -e "${YELLOW}Note: Install 'jq' for better JSON formatting${NC}"
        return 1
    fi
}

# 1. Health Check
echo -e "${GREEN}1. Health Check${NC}"
echo "Endpoint: GET /health"
echo "Command: curl $GATEWAY_URL/health"
echo

response=$(curl -s "$GATEWAY_URL/health")
if check_jq; then
    echo "$response" | jq .
else
    echo "$response"
fi
echo

# 2. List Available Tools
echo -e "${GREEN}2. List Available Tools${NC}"
echo "Endpoint: GET /mcp/tools"
echo "Command: curl -H \"Authorization: Bearer \$API_KEY\" $GATEWAY_URL/mcp/tools"
echo

response=$(make_request "GET" "/mcp/tools")
if check_jq; then
    echo "$response" | head -n -1 | jq .
    echo "$(echo "$response" | tail -n 1)"
else
    echo "$response"
fi
echo

# 3. List Available Models
echo -e "${GREEN}3. List Available Models${NC}"
echo "Endpoint: POST /tools/list_models"
echo "Command: curl -X POST -H \"Authorization: Bearer \$API_KEY\" -H \"Content-Type: application/json\" -d '{\"parameters\":{}}' $GATEWAY_URL/tools/list_models"
echo

response=$(make_request "POST" "/tools/list_models" '{"parameters":{}}')
if check_jq; then
    echo "$response" | head -n -1 | jq .
    echo "$(echo "$response" | tail -n 1)"
else
    echo "$response"
fi
echo

# Extract first model for text generation example
if check_jq; then
    first_model=$(echo "$response" | head -n -1 | jq -r '.result.models[0].id // "unknown"')
else
    # Simple extraction without jq (less reliable)
    first_model=$(echo "$response" | grep -o '"id":"[^"]*"' | head -1 | cut -d'"' -f4)
    if [ -z "$first_model" ]; then
        first_model="unknown"
    fi
fi

# 4. Generate Text
echo -e "${GREEN}4. Generate Text${NC}"
echo "Endpoint: POST /tools/inference"
echo "Using model: $first_model"

if [ "$first_model" != "unknown" ] && [ -n "$first_model" ]; then
    inference_data='{
        "parameters": {
            "prompt": "Write a short poem about artificial intelligence.",
            "model": "'$first_model'",
            "temperature": 0.8,
            "max_tokens": 200
        }
    }'
    
    echo "Command: curl -X POST -H \"Authorization: Bearer \$API_KEY\" -H \"Content-Type: application/json\" -d '$inference_data' $GATEWAY_URL/tools/inference"
    echo
    
    response=$(make_request "POST" "/tools/inference" "$inference_data")
    if check_jq; then
        echo "$response" | head -n -1 | jq .
        echo "$(echo "$response" | tail -n 1)"
    else
        echo "$response"
    fi
else
    echo "No models available for text generation"
fi
echo

# 5. Error Handling Examples
echo -e "${GREEN}5. Error Handling Examples${NC}"
echo

# Invalid endpoint
echo -e "${YELLOW}5a. Invalid Endpoint (404 Error)${NC}"
echo "Command: curl $GATEWAY_URL/invalid/endpoint"
response=$(curl -s -w "\nHTTP Status: %{http_code}\n" "$GATEWAY_URL/invalid/endpoint")
echo "$response"
echo

# Missing authentication
echo -e "${YELLOW}5b. Missing Authentication (401 Error)${NC}"
echo "Command: curl $GATEWAY_URL/mcp/tools"
response=$(curl -s -w "\nHTTP Status: %{http_code}\n" "$GATEWAY_URL/mcp/tools")
echo "$response"
echo

# Invalid JSON
echo -e "${YELLOW}5c. Invalid JSON (400 Error)${NC}"
echo "Command: curl -X POST -H \"Authorization: Bearer \$API_KEY\" -H \"Content-Type: application/json\" -d 'invalid json' $GATEWAY_URL/tools/inference"
response=$(curl -s -w "\nHTTP Status: %{http_code}\n" \
           -X POST \
           -H "Authorization: Bearer $API_KEY" \
           -H "Content-Type: application/json" \
           -d 'invalid json' \
           "$GATEWAY_URL/tools/inference")
echo "$response"
echo

# 6. Advanced Examples
echo -e "${GREEN}6. Advanced Examples${NC}"
echo

# Streaming request (if supported)
echo -e "${YELLOW}6a. Streaming Request${NC}"
if [ "$first_model" != "unknown" ] && [ -n "$first_model" ]; then
    streaming_data='{
        "parameters": {
            "prompt": "Count from 1 to 5.",
            "model": "'$first_model'",
            "stream": true,
            "max_tokens": 50
        }
    }'
    
    echo "Command: curl -X POST -H \"Authorization: Bearer \$API_KEY\" -H \"Content-Type: application/json\" -d '$streaming_data' $GATEWAY_URL/tools/inference"
    echo
    
    response=$(make_request "POST" "/tools/inference" "$streaming_data")
    if check_jq; then
        echo "$response" | head -n -1 | jq .
        echo "$(echo "$response" | tail -n 1)"
    else
        echo "$response"
    fi
else
    echo "No models available for streaming example"
fi
echo

# Performance test
echo -e "${YELLOW}6b. Performance Test (Multiple Requests)${NC}"
echo "Making 3 concurrent requests..."

if [ "$first_model" != "unknown" ] && [ -n "$first_model" ]; then
    perf_data='{
        "parameters": {
            "prompt": "Hello!",
            "model": "'$first_model'",
            "max_tokens": 10
        }
    }'
    
    # Make 3 concurrent requests
    for i in {1..3}; do
        (
            start_time=$(date +%s.%N)
            response=$(make_request "POST" "/tools/inference" "$perf_data" 2>/dev/null)
            end_time=$(date +%s.%N)
            duration=$(echo "$end_time - $start_time" | bc 2>/dev/null || echo "N/A")
            echo "Request $i: ${duration}s"
        ) &
    done
    wait
else
    echo "No models available for performance test"
fi
echo

echo -e "${BLUE}Examples completed!${NC}"
echo
echo -e "${YELLOW}Tips:${NC}"
echo "- Install 'jq' for better JSON formatting: apt-get install jq (Ubuntu) or brew install jq (macOS)"
echo "- Set API_KEY environment variable: export API_KEY=your-api-key"
echo "- Set GATEWAY_URL environment variable: export GATEWAY_URL=http://your-gateway:8080"
echo "- Use -v flag with curl for verbose output: curl -v ..."
echo "- Use --fail flag to exit on HTTP errors: curl --fail ..."
