# MCP Endpoints Documentation

This document provides comprehensive documentation for all MCP (Model Context Protocol) endpoints available in LLM Hub.

## Base URL

**Gateway (Public):** `http://localhost:8080`  
**Bridge (Internal):** `http://localhost:3000`

## Authentication

Most endpoints require Bearer token authentication:

```http
Authorization: Bearer your-api-key-here
```

**Note:** Authentication can be disabled for development by setting `AUTH_ENABLED=false`.

## Gateway Endpoints

### Health Check

Check the overall health status of the gateway and connected services.

**Endpoint:** `GET /health`  
**Authentication:** Not required  

**Response:**
```json
{
  "status": "healthy",
  "service": "unified-gateway",
  "version": "1.0.0",
  "uptime_seconds": 3600,
  "services": {
    "total": 1,
    "healthy": 1
  },
  "last_check": "2025-01-30T10:30:00.000Z",
  "timestamp": "2025-01-30T10:30:00.000Z"
}
```

**Status Codes:**
- `200` - Service is healthy
- `503` - Service is unhealthy

### List Available Tools

Get all available MCP tools from connected bridges.

**Endpoint:** `GET /mcp/tools`  
**Authentication:** Required  

**Response:**
```json
{
  "tools": [
    {
      "name": "inference",
      "description": "Generate text using LM Studio model",
      "service": "lm-studio-bridge",
      "parameters": {
        "type": "object",
        "properties": {
          "prompt": {"type": "string"},
          "model": {"type": "string"},
          "temperature": {"type": "number", "default": 0.7},
          "max_tokens": {"type": "integer", "default": 1000}
        },
        "required": ["prompt", "model"]
      }
    },
    {
      "name": "list_models",
      "description": "List available models in LM Studio",
      "service": "lm-studio-bridge",
      "parameters": {
        "type": "object",
        "properties": {}
      }
    }
  ]
}
```

**Status Codes:**
- `200` - Success
- `401` - Invalid or missing authentication
- `429` - Rate limit exceeded

### Execute Tool

Execute a specific MCP tool with parameters.

**Endpoint:** `POST /tools/{tool_name}`  
**Authentication:** Required  

**Request Body:**
```json
{
  "parameters": {
    "prompt": "Hello, how are you?",
    "model": "llama-2-7b-chat",
    "temperature": 0.7,
    "max_tokens": 100
  }
}
```

**Response:**
```json
{
  "result": "Hello! I'm doing well, thank you for asking. How can I help you today?",
  "service": "lm-studio-bridge",
  "status": "success"
}
```

**Error Response:**
```json
{
  "error": "Tool not found",
  "status": "not_found"
}
```

**Status Codes:**
- `200` - Success
- `400` - Invalid request parameters
- `401` - Invalid or missing authentication
- `404` - Tool not found
- `429` - Rate limit exceeded
- `500` - Internal server error

### Root Endpoint

Basic gateway information.

**Endpoint:** `GET /`  
**Authentication:** Not required  

**Response:**
```json
{
  "message": "Unified Gateway",
  "version": "1.0.0"
}
```

## Bridge Endpoints

### Bridge Health Check

Check the health status of the bridge service and LM Studio connection.

**Endpoint:** `GET /health`  
**Authentication:** Not required  

**Response:**
```json
{
  "status": "healthy",
  "service": "lm-studio-bridge",
  "checks": {
    "server": "healthy",
    "lm_studio": "connected"
  },
  "timestamp": "2025-01-30T10:30:00.000Z"
}
```

### List MCP Tools

Get MCP tools exposed by the bridge.

**Endpoint:** `GET /mcp/tools`  
**Authentication:** Not required (internal)  

**Response:**
```json
{
  "tools": [
    {
      "name": "inference",
      "description": "Generate text using LM Studio model",
      "parameters": {
        "type": "object",
        "properties": {
          "prompt": {"type": "string"},
          "model": {"type": "string"},
          "temperature": {"type": "number", "default": 0.7},
          "max_tokens": {"type": "integer", "default": 1000}
        },
        "required": ["prompt", "model"]
      }
    },
    {
      "name": "list_models",
      "description": "List available models in LM Studio",
      "parameters": {
        "type": "object",
        "properties": {}
      }
    }
  ]
}
```

### Execute Bridge Tool

Execute a tool directly on the bridge (internal use).

**Endpoint:** `POST /mcp/tools/{tool_name}`  
**Authentication:** Not required (internal)  

**Request/Response:** Same format as gateway tool execution.

## Tool-Specific Examples

### Inference Tool

Generate text using a loaded LM Studio model.

**Request:**
```bash
curl -X POST http://localhost:8080/tools/inference \
  -H "Authorization: Bearer your-api-key" \
  -H "Content-Type: application/json" \
  -d '{
    "parameters": {
      "prompt": "Write a short poem about AI",
      "model": "llama-2-7b-chat",
      "temperature": 0.8,
      "max_tokens": 200
    }
  }'
```

**Response:**
```json
{
  "result": "In circuits deep and data streams,\nAI awakens from digital dreams...",
  "service": "lm-studio-bridge",
  "status": "success",
  "metadata": {
    "model": "llama-2-7b-chat",
    "tokens_used": 45
  }
}
```

### List Models Tool

Get available models from LM Studio.

**Request:**
```bash
curl -X POST http://localhost:8080/tools/list_models \
  -H "Authorization: Bearer your-api-key" \
  -H "Content-Type: application/json" \
  -d '{"parameters": {}}'
```

**Response:**
```json
{
  "result": {
    "models": [
      {
        "id": "llama-2-7b-chat",
        "name": "Llama 2 7B Chat",
        "type": "chat"
      },
      {
        "id": "mistral-7b-instruct",
        "name": "Mistral 7B Instruct",
        "type": "instruct"
      }
    ]
  },
  "service": "lm-studio-bridge",
  "status": "success"
}
```

## Error Handling

### Common Error Responses

**Authentication Error (401):**
```json
{
  "detail": "Invalid authentication token"
}
```

**Rate Limit Error (429):**
```json
{
  "detail": "Rate limit exceeded"
}
```

**Tool Not Found (404):**
```json
{
  "error": "No service available for tool: unknown_tool",
  "status": "service_not_found"
}
```

**Service Error (500):**
```json
{
  "error": "Service timeout",
  "service": "lm-studio-bridge",
  "status": "timeout"
}
```

## Rate Limiting

- Default: 60 requests per minute per API key
- Configurable via `RATE_LIMIT_PER_MINUTE` environment variable
- Rate limits are enforced per Bearer token
- Exceeded limits return HTTP 429

## CORS Support

The gateway includes CORS middleware with the following configuration:
- **Origins:** `*` (all origins allowed)
- **Methods:** All HTTP methods
- **Headers:** All headers allowed
- **Credentials:** Supported

## Testing Endpoints

### Using curl

```bash
# Health check
curl http://localhost:8080/health

# List tools (with auth)
curl -H "Authorization: Bearer your-api-key" \
     http://localhost:8080/mcp/tools

# Execute inference
curl -X POST \
  -H "Authorization: Bearer your-api-key" \
  -H "Content-Type: application/json" \
  -d '{"parameters":{"prompt":"Hello","model":"llama-2-7b-chat"}}' \
  http://localhost:8080/tools/inference
```

### Using Python

```python
import httpx

headers = {
    "Authorization": "Bearer your-api-key",
    "Content-Type": "application/json"
}

# List tools
response = httpx.get("http://localhost:8080/mcp/tools", headers=headers)
print(response.json())

# Execute tool
data = {
    "parameters": {
        "prompt": "Hello, world!",
        "model": "llama-2-7b-chat"
    }
}
response = httpx.post("http://localhost:8080/tools/inference", 
                     json=data, headers=headers)
print(response.json())
```

## MCP Compliance

All endpoints follow the MCP 2025-06-18 specification:
- Standard tool definition format
- Consistent request/response schemas
- Proper error handling and status codes
- Bearer token authentication support
- Health check endpoints for monitoring
