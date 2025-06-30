# LLM Hub Architecture Overview

This document provides a comprehensive overview of the LLM Hub system architecture, component interactions, and data flow.

## System Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   MCP Client    │    │   Web Browser   │    │  Direct Client  │
│   Application   │    │   Dashboard     │    │   (curl/API)   │
└─────────┬───────┘    └─────────┬───────┘    └─────────┬───────┘
          │                      │                      │
          │ MCP Protocol         │ HTTP/REST            │ HTTP/REST
          │                      │                      │
          └──────────────────────┼──────────────────────┘
                                 │
                    ┌────────────▼────────────┐
                    │   Unified Gateway       │
                    │   (Port 8080)          │
                    │   - Authentication     │
                    │   - Rate Limiting      │
                    │   - Request Routing    │
                    │   - Load Balancing     │
                    └────────────┬────────────┘
                                 │
                                 │ Internal HTTP
                                 │
                    ┌────────────▼────────────┐
                    │   LM Studio Bridge     │
                    │   (Port 3000)          │
                    │   - Model Discovery    │
                    │   - MCP Tool Exposure  │
                    │   - Request Translation│
                    └────────────┬────────────┘
                                 │
                                 │ OpenAI API
                                 │
                    ┌────────────▼────────────┐
                    │     LM Studio          │
                    │     (Port 1234)        │
                    │   - Model Hosting      │
                    │   - Inference Engine   │
                    │   - Local Processing   │
                    └─────────────────────────┘
```

## Component Descriptions

### Unified Gateway
**Purpose:** Central API gateway providing unified access to all LLM services

**Responsibilities:**
- Client authentication and authorization
- Request rate limiting and throttling
- Service discovery and health monitoring
- Load balancing across multiple bridges
- Request routing to appropriate backend services
- Response aggregation and formatting

**Key Features:**
- Bearer token authentication
- Configurable rate limits per API key
- Health check endpoints
- CORS support for web applications
- Automatic service discovery

### LM Studio Bridge
**Purpose:** Protocol bridge between MCP and LM Studio's OpenAI-compatible API

**Responsibilities:**
- Automatic model discovery from LM Studio
- MCP tool definition and exposure
- Request translation between MCP and OpenAI formats
- Response formatting for MCP compliance
- Health monitoring of LM Studio connection

**Key Features:**
- Periodic model polling (30-second intervals)
- Dynamic tool registration
- Streaming response support
- Error handling and retry logic
- MCP 2025-06-18 specification compliance

### LM Studio
**Purpose:** Local LLM hosting and inference engine

**Responsibilities:**
- Model loading and management
- Text generation and completion
- Local inference processing
- OpenAI-compatible API provision

**Integration Points:**
- HTTP API on port 1234
- Model listing via `/v1/models`
- Text completion via `/v1/completions`
- Streaming support for real-time responses

## Data Flow

### Model Discovery Flow
```
1. Bridge polls LM Studio every 30 seconds
2. Retrieves available models via /v1/models
3. Converts models to MCP tool definitions
4. Registers tools with internal registry
5. Gateway discovers new tools via bridge health checks
6. Tools become available through gateway endpoints
```

### Request Processing Flow
```
1. Client sends MCP request to Gateway (port 8080)
2. Gateway validates authentication and rate limits
3. Gateway routes request to appropriate Bridge (port 3000)
4. Bridge translates MCP request to OpenAI format
5. Bridge forwards request to LM Studio (port 1234)
6. LM Studio processes inference and returns response
7. Bridge translates response back to MCP format
8. Gateway returns formatted response to client
```

## Port Mappings

| Service | Internal Port | External Port | Protocol | Purpose |
|---------|---------------|---------------|----------|---------|
| Unified Gateway | 8080 | 8080 | HTTP | Public API access |
| LM Studio Bridge | 3000 | 3000 | HTTP | Internal service communication |
| LM Studio | 1234 | 1234 | HTTP | Local model inference |

## Network Architecture

### Docker Network
- **Name:** `llm-hub-net`
- **Type:** Bridge network
- **Subnet:** `172.20.0.0/16`
- **DNS:** Automatic service discovery

### Service Communication
- **Gateway ↔ Bridge:** Internal HTTP via Docker network
- **Bridge ↔ LM Studio:** Host network access via `host.docker.internal`
- **Client ↔ Gateway:** External HTTP via published ports

## Security Model

### Authentication
- Bearer token authentication required for all API endpoints
- Configurable API keys via environment variables
- Optional authentication bypass for development

### Network Security
- Services isolated within Docker network
- Only gateway exposes public endpoints
- Internal communication encrypted via Docker network

### Rate Limiting
- Per-token rate limiting (default: 60 requests/minute)
- Configurable limits via environment variables
- Automatic request throttling and rejection

## Scalability Considerations

### Horizontal Scaling
- Multiple bridge instances can be deployed
- Gateway provides automatic load balancing
- Round-robin distribution across healthy bridges

### Vertical Scaling
- Resource limits configurable via Docker Compose
- Memory and CPU allocation per service
- Automatic restart on resource exhaustion

### Performance Optimization
- Connection pooling for backend requests
- Response caching for model metadata
- Asynchronous request processing
- Streaming support for large responses

## Monitoring and Health Checks

### Health Endpoints
- Gateway: `GET /health` - Overall system health
- Bridge: `GET /health` - Bridge and LM Studio connectivity
- Automatic health check intervals (30 seconds)

### Logging
- Structured JSON logging
- Configurable log levels (DEBUG, INFO, WARN, ERROR)
- Centralized log collection via Docker volumes
- Request/response tracing for debugging

### Metrics
- Request count and latency tracking
- Error rate monitoring
- Service availability metrics
- Resource utilization monitoring

## Deployment Architecture

### Container Strategy
- Multi-stage Docker builds for optimized images
- Alpine Linux base for minimal footprint
- Health check integration with Docker Compose
- Automatic restart policies

### Volume Management
- Persistent log storage
- Configuration file mounting
- Shared data volumes between services

### Environment Configuration
- Environment-based configuration
- Secrets management via environment variables
- Development vs production configurations
