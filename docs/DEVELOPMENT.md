# LLM Hub Development Guide

This guide is for developers who want to add new features or extend units in LLM Hub.

## Development Environment Setup

### Prerequisites

- Windows 10/11 with WSL2 or Linux development environment
- Docker Desktop
- Python 3.11+
- Git
- Visual Studio Code (recommended)

### Local Development Setup

1. **Clone Repository**
   ```bash
   git clone https://github.com/your-org/llm-hub.git
   cd llm-hub
   ```

2. **Set Up Development Environment**
   ```bash
   # Copy environment template
   cp ops/compose/.env.example ops/compose/.env
   
   # Edit for development
   # Set AUTH_ENABLED=false for easier testing
   # Set LOG_LEVEL=DEBUG for verbose logging
   ```

3. **Install Development Dependencies**
   ```bash
   # For each unit you want to develop
   cd units/lm-studio-bridge
   pip install -r requirements.txt
   pip install -e .
   ```

## Architecture Overview

LLM Hub follows the **dedardf** methodology with strict separation of concerns:

### Directory Structure

```
llm-hub/
├── platform/           # Core platform components
│   ├── core/           # Base classes and utilities
│   ├── runtime/        # Runtime management
│   └── contracts/      # Service contracts
├── units/              # Independent service units
│   ├── lm-studio-bridge/
│   └── unified-gateway/
├── shared/             # Shared utilities and libraries
├── ops/                # Operations and deployment
│   ├── scripts/        # Automation scripts
│   └── compose/        # Docker Compose configurations
└── docs/               # Documentation
```

### dedardf Principles

1. **Decoupled** - Units operate independently
2. **Declarative** - Configuration over code
3. **Atomic** - Single responsibility per unit
4. **Resilient** - Graceful failure handling
5. **Discoverable** - Self-describing services
6. **Federated** - Distributed architecture

## Adding a New Unit

### Step 1: Create Unit Structure

```bash
mkdir units/my-new-unit
cd units/my-new-unit

# Create required files
touch unit.yml
touch mcp-validation.yml
touch Dockerfile
touch start.sh
touch requirements.txt
mkdir api config logic
```

### Step 2: Define Unit Contract

Create `unit.yml`:

```yaml
id: "my-new-unit"
version: "1.0.0"
type: "mcp-service"
description: "Description of your new unit"

contracts:
  exposes:
    - "my-service.v1"
  consumes:
    - "discovery.v1"

entrypoint: "./start.sh"

mcp:
  enabled: true
  sdk: "python"
  spec_version: "2025-06-18"

runtime:
  platform: "python"
  version: "3.11"

dependencies:
  - "mcp>=1.0.0"
  - "fastmcp>=2.0.0"
  - "httpx>=0.25.0"

ports:
  service: 4000

environment:
  required:
    - "SERVICE_URL"
  optional:
    - "LOG_LEVEL"
    - "POLL_INTERVAL"

health_check:
  path: "/health"
  interval: 30
  timeout: 10
  retries: 3
```

### Step 3: Create Service Contract

Create `platform/contracts/my-service.v1.yml`:

```yaml
name: "my-service"
version: "1.0.0"
description: "Contract for my new service"
spec_version: "2025-06-18"

endpoints:
  health:
    path: "/health"
    method: "GET"
    description: "Service health check"
    
  tools:
    path: "/mcp/tools"
    method: "GET"
    description: "List available tools"
    
  execute:
    path: "/mcp/tools/{tool_name}"
    method: "POST"
    description: "Execute tool"
```

### Step 4: Implement MCP Validation

Create `mcp-validation.yml`:

```yaml
sdk: "python"
spec_version: "2025-06-18"

checks:
  sdk-version:
    description: "Validate MCP SDK version compatibility"
    requirement: ">=1.0.0"
    critical: true
    
  exposes-api:
    description: "Validate all MCP endpoints are exposed"
    endpoints:
      - "/health"
      - "/mcp/tools"
    critical: true
    
  contract-alignment:
    description: "Validate alignment with service contract"
    contract: "my-service.v1"
    critical: true
```

### Step 5: Implement Service Logic

Create the main service files:

- `api/server.py` - FastMCP server implementation
- `logic/service_logic.py` - Business logic
- `config/settings.py` - Configuration management

### Step 6: Add to Docker Compose

Update `ops/compose/docker-compose.yml`:

```yaml
services:
  my-new-unit:
    build:
      context: ../../units/my-new-unit
      dockerfile: Dockerfile
    container_name: my-new-unit
    networks:
      - llm-hub-net
    environment:
      - SERVICE_URL=${MY_SERVICE_URL}
      - LOG_LEVEL=${LOG_LEVEL:-INFO}
    ports:
      - "4000:4000"
    healthcheck:
      test: ["CMD", "wget", "-q", "--spider", "http://localhost:4000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
```

## Extending Existing Units

### Adding New Tools

1. **Define Tool in Bridge**
   ```python
   @self.mcp.tool()
   async def my_new_tool(param1: str, param2: int = 10) -> dict:
       """Description of the new tool"""
       # Implementation
       return {"result": "success"}
   ```

2. **Update Tool Registry**
   Add tool definition to `/mcp/tools` endpoint response.

3. **Add Routing Rules**
   Update gateway routing in `platform/contracts/gateway.v1.yml`.

### Adding New Endpoints

1. **Define in Contract**
   Add endpoint definition to relevant contract file.

2. **Implement Handler**
   ```python
   @app.get("/my/new/endpoint")
   async def my_endpoint():
       return {"message": "Hello from new endpoint"}
   ```

3. **Update Validation**
   Add endpoint to `mcp-validation.yml` checks.

## Testing

### Unit Testing

```bash
# Run unit tests for a specific unit
cd units/lm-studio-bridge
python -m pytest tests/

# Run with coverage
python -m pytest --cov=api --cov=logic tests/
```

### Integration Testing

```bash
# Run full integration test suite
cd ops/scripts
bash run-all-tests.sh

# Run specific test
python3 inference-test.py
```

### Manual Testing

```bash
# Start services in development mode
docker-compose up --build

# Test endpoints
curl http://localhost:8080/health
curl -H "Authorization: Bearer changeme" http://localhost:8080/mcp/tools
```

## Code Style and Standards

### Python Code Style

- Follow PEP 8
- Use type hints
- Document functions with docstrings
- Use async/await for I/O operations

### Example Code Structure

```python
"""
Module Description
Brief description of what this module does
"""

import logging
from typing import Dict, Any, Optional
from fastapi import HTTPException

logger = logging.getLogger(__name__)

class ServiceManager:
    """Manages service operations"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.logger = logger
    
    async def process_request(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Process incoming request
        
        Args:
            data: Request data dictionary
            
        Returns:
            Processed response dictionary
            
        Raises:
            HTTPException: If processing fails
        """
        try:
            # Implementation
            return {"status": "success"}
        except Exception as e:
            self.logger.error(f"Processing failed: {e}")
            raise HTTPException(status_code=500, detail="Processing failed")
```

### Configuration Management

```python
import os
from typing import Optional

class Settings:
    """Service configuration settings"""
    
    def __init__(self):
        self.service_url: str = os.getenv("SERVICE_URL", "http://localhost:4000")
        self.log_level: str = os.getenv("LOG_LEVEL", "INFO")
        self.poll_interval: int = int(os.getenv("POLL_INTERVAL", "30"))
    
    def validate(self) -> None:
        """Validate configuration"""
        if not self.service_url:
            raise ValueError("SERVICE_URL is required")
```

## Debugging

### Local Debugging

1. **Set Debug Environment**
   ```bash
   export LOG_LEVEL=DEBUG
   export AUTH_ENABLED=false
   ```

2. **Run Service Locally**
   ```bash
   cd units/my-unit
   python -m api.server
   ```

3. **Attach Debugger**
   Use VS Code debugger or pdb for step-through debugging.

### Container Debugging

```bash
# View logs
docker-compose logs my-new-unit

# Execute into container
docker-compose exec my-new-unit /bin/sh

# Debug with verbose output
docker-compose up my-new-unit --build
```

## Contributing Guidelines

### Pull Request Process

1. **Create Feature Branch**
   ```bash
   git checkout -b feature/my-new-feature
   ```

2. **Make Changes**
   - Follow coding standards
   - Add tests for new functionality
   - Update documentation

3. **Test Changes**
   ```bash
   # Run validation
   ops/scripts/rule0-check.sh
   ops/scripts/mcp-compliance-test.sh
   ops/scripts/run-all-tests.sh
   ```

4. **Submit PR**
   - Clear description of changes
   - Reference any related issues
   - Include test results

### Code Review Checklist

- [ ] Follows dedardf principles
- [ ] Includes appropriate tests
- [ ] Documentation updated
- [ ] MCP compliance maintained
- [ ] No breaking changes to existing contracts
- [ ] Performance impact considered
- [ ] Security implications reviewed

## Common Patterns

### Error Handling

```python
from platform.core.exceptions import PlatformError

try:
    result = await external_service_call()
except httpx.TimeoutException:
    raise PlatformError("Service timeout", code="TIMEOUT")
except Exception as e:
    logger.error(f"Unexpected error: {e}")
    raise PlatformError("Internal error", code="INTERNAL_ERROR")
```

### Configuration Injection

```python
from platform.core.config import get_config

class MyService:
    def __init__(self):
        self.config = get_config("my-service")
        self.api_url = self.config.get("api_url")
```

### Health Checks

```python
@app.get("/health")
async def health_check():
    """Standard health check implementation"""
    try:
        # Check dependencies
        await check_external_service()
        
        return {
            "status": "healthy",
            "service": "my-service",
            "version": "1.0.0",
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }
```

## Resources

- [MCP Specification 2025-06-18](https://spec.modelcontextprotocol.io/)
- [FastMCP Documentation](https://fastmcp.readthedocs.io/)
- [Docker Compose Reference](https://docs.docker.com/compose/)
- [dedardf Methodology](docs/architecture/decisions/ADR-001-minimal-platform.md)
