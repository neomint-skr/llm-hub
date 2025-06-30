# LLM Hub Configuration Guide

This guide explains all environment variables and configuration options available in LLM Hub.

## Configuration Files

LLM Hub uses environment variables for configuration, managed through these files:

- `ops/compose/.env` - Main configuration file (created from .env.example)
- `ops/compose/.env.example` - Template with default values and documentation
- `units/*/config/env.default` - Service-specific default configurations

## Environment Variables Reference

### LM Studio Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `LM_STUDIO_URL` | `http://host.docker.internal:1234` | URL to LM Studio API endpoint. Use `host.docker.internal` for Docker Desktop on Windows/Mac, or your host IP for native Docker on Linux. |

**Example Values:**
```bash
# Docker Desktop (Windows/Mac)
LM_STUDIO_URL=http://host.docker.internal:1234

# Native Docker (Linux)
LM_STUDIO_URL=http://192.168.1.100:1234

# Custom port
LM_STUDIO_URL=http://host.docker.internal:1235
```

### Bridge Service Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `MCP_PORT` | `3000` | Port for LM Studio Bridge service (internal Docker network) |
| `POLL_INTERVAL` | `30` | Interval in seconds for model discovery polling. Lower values = more frequent checks but higher CPU usage. |

**Performance Tuning:**
```bash
# High-frequency updates (development)
POLL_INTERVAL=10

# Standard updates (production)
POLL_INTERVAL=30

# Low-frequency updates (resource-constrained)
POLL_INTERVAL=60
```

### Gateway Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `GATEWAY_PORT` | `8080` | Port for unified gateway service (public endpoint) |
| `API_KEY` | `changeme` | API key for bearer token authentication. **Must be changed in production!** |
| `AUTH_ENABLED` | `true` | Enable/disable gateway authentication. Set to `false` for development only. |
| `RATE_LIMIT_PER_MINUTE` | `60` | Maximum requests per minute per API key |
| `BRIDGE_URL` | `http://lm-studio-bridge:3000` | Internal URL to bridge service (Docker network) |

**Security Configuration:**
```bash
# Generate secure API key
API_KEY=$(openssl rand -hex 32)

# Production settings
AUTH_ENABLED=true
RATE_LIMIT_PER_MINUTE=120

# Development settings (NOT for production)
AUTH_ENABLED=false
RATE_LIMIT_PER_MINUTE=1000
```

### Logging Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `LOG_LEVEL` | `INFO` | Log level for all services. Options: `DEBUG`, `INFO`, `WARNING`, `ERROR` |

**Log Level Guidelines:**
```bash
# Development and troubleshooting
LOG_LEVEL=DEBUG

# Production (recommended)
LOG_LEVEL=INFO

# Production (minimal logging)
LOG_LEVEL=WARNING

# Critical errors only
LOG_LEVEL=ERROR
```

### Service Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `SERVICE_NAME` | Auto-set | Service name for logging and discovery (automatically set per service) |

## Configuration Examples

### Development Environment

```bash
# ops/compose/.env
LM_STUDIO_URL=http://host.docker.internal:1234
GATEWAY_PORT=8080
MCP_PORT=3000
API_KEY=dev-key-12345
AUTH_ENABLED=false
RATE_LIMIT_PER_MINUTE=1000
POLL_INTERVAL=10
LOG_LEVEL=DEBUG
```

### Production Environment

```bash
# ops/compose/.env
LM_STUDIO_URL=http://host.docker.internal:1234
GATEWAY_PORT=8080
MCP_PORT=3000
API_KEY=your-very-secure-random-key-here
AUTH_ENABLED=true
RATE_LIMIT_PER_MINUTE=60
POLL_INTERVAL=30
LOG_LEVEL=INFO
```

### High-Performance Environment

```bash
# ops/compose/.env
LM_STUDIO_URL=http://host.docker.internal:1234
GATEWAY_PORT=8080
MCP_PORT=3000
API_KEY=your-secure-key
AUTH_ENABLED=true
RATE_LIMIT_PER_MINUTE=300
POLL_INTERVAL=15
LOG_LEVEL=WARNING
```

## Advanced Configuration

### Custom Ports

If default ports conflict with other services:

```bash
# Change gateway port
GATEWAY_PORT=8081

# Change bridge port (also update BRIDGE_URL)
MCP_PORT=3001
BRIDGE_URL=http://lm-studio-bridge:3001
```

**Note:** When changing `MCP_PORT`, you must also update the port mapping in `docker-compose.yml`:

```yaml
services:
  lm-studio-bridge:
    ports:
      - "3001:3001"  # Change from 3000:3000
```

### Multiple API Keys

For multiple clients with different rate limits, you can implement custom authentication logic or use a reverse proxy. The current implementation supports one API key per deployment.

### Resource Limits

Configure Docker resource limits in `docker-compose.yml`:

```yaml
services:
  unified-gateway:
    deploy:
      resources:
        limits:
          memory: 512M
          cpus: '0.5'
        reservations:
          memory: 256M
          cpus: '0.25'
```

### Network Configuration

For custom network setups, modify the Docker Compose network configuration:

```yaml
networks:
  llm-hub-net:
    driver: bridge
    ipam:
      config:
        - subnet: 172.21.0.0/16  # Custom subnet
```

## Configuration Validation

### Required Variables

The following variables must be set:

**Gateway:**
- `API_KEY` (must not be default value in production)
- `BRIDGE_URL`

**Bridge:**
- `LM_STUDIO_URL`

### Validation Commands

```bash
# Check configuration
docker-compose config

# Validate environment variables
docker-compose run --rm unified-gateway env

# Test connectivity
curl http://localhost:8080/health
```

## Troubleshooting Configuration

### Common Issues

1. **Services won't start**
   - Check for missing required variables
   - Verify port availability
   - Check Docker network configuration

2. **Authentication failures**
   - Verify `API_KEY` is set correctly
   - Check `AUTH_ENABLED` setting
   - Ensure Bearer token format: `Authorization: Bearer your-api-key`

3. **Connection issues**
   - Verify `LM_STUDIO_URL` points to running LM Studio
   - Check `BRIDGE_URL` for internal service communication
   - Ensure firewall allows required ports

### Configuration Testing

```bash
# Test LM Studio connection
curl $LM_STUDIO_URL/v1/models

# Test bridge health
curl http://localhost:$MCP_PORT/health

# Test gateway health
curl http://localhost:$GATEWAY_PORT/health

# Test authenticated endpoint
curl -H "Authorization: Bearer $API_KEY" \
     http://localhost:$GATEWAY_PORT/mcp/tools
```

## Security Best Practices

1. **Always change default API key in production**
2. **Use strong, randomly generated API keys**
3. **Enable authentication in production (`AUTH_ENABLED=true`)**
4. **Set appropriate rate limits for your use case**
5. **Use `INFO` or `WARNING` log level in production**
6. **Regularly rotate API keys**
7. **Monitor logs for suspicious activity**

## Performance Tuning

### High-Traffic Scenarios

```bash
# Increase rate limits
RATE_LIMIT_PER_MINUTE=300

# Reduce polling frequency to save resources
POLL_INTERVAL=60

# Minimize logging
LOG_LEVEL=WARNING
```

### Low-Resource Scenarios

```bash
# Conservative rate limits
RATE_LIMIT_PER_MINUTE=30

# Longer polling intervals
POLL_INTERVAL=120

# Minimal logging
LOG_LEVEL=ERROR
```

### Real-Time Applications

```bash
# Frequent model discovery
POLL_INTERVAL=10

# Higher rate limits
RATE_LIMIT_PER_MINUTE=600

# Detailed logging for monitoring
LOG_LEVEL=INFO
```
