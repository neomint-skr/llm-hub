```yaml
task: "3.1_create_gateway_unit_structure"
directory: "units/unified-gateway/"
goal: |
  Erstelle vollständige Unit-Verzeichnisstruktur für
  Unified-Gateway analog zur Bridge-Unit mit allen Verzeichnissen.
tools: |
  - mkdir für Verzeichnisse
  - touch für Placeholder-Dateien
  - Struktur: api/, logic/, config/
work: |
  200 Token (Struktur erstellen)
negative_constraints: |
  - KEINE Dateien mit Inhalt
  - KEINE Bridge-spezifischen Verzeichnisse
  - KEINE Cross-Unit-Referenzen
validation: |
  Negative Constraints:
  - Keine Inhalte in Dateien
  - Keine Extra-Verzeichnisse
  Positive Constraints:
  - api/, logic/, config/ Verzeichnisse
  - .gitkeep in leeren Verzeichnissen
  - Parallel zu Bridge-Struktur
  GUTWILLIG:
  - Konsistente Unit-Struktur
  INTELLIGENT:
  - Gleiche Struktur wie Bridge
  KONTEXT-AWARE:
  - dedardf-konforme Unit
  FAUL:
  - Nur Struktur
fallback: |
  Bei fehlenden Dirs: Nacherstellen
```

```yaml
task: "3.2_create_gateway_manifest"
directory: "units/unified-gateway/"
goal: |
  Erstelle unit.yml für Gateway mit Public Port Configuration
  und Referenzen zu Bridge-Services.
tools: |
  - Datei: units/unified-gateway/unit.yml
  - YAML-Format
  - Gateway-Type Declaration
work: |
  400 Token (Gateway-Manifest)
negative_constraints: |
  - KEINE direkten Unit-Dependencies
  - KEINE Bridge-Implementation
  - KEINE hartkodierten URLs
validation: |
  Negative Constraints:
  - Keine Direct Dependencies
  - Keine Implementation
  Positive Constraints:
  - id: "unified-gateway"
  - version: "1.0.0"
  - type: "mcp-gateway"
  - contracts: exposes["gateway.v1"], consumes["lm-bridge.v1", "discovery.v1"]
  - ports: public: 8080
  - mcp: true
  GUTWILLIG:
  - Gateway-Definition
  INTELLIGENT:
  - Service-Aggregation vorbereitet
  KONTEXT-AWARE:
  - Nutzt Platform-Contracts
  FAUL:
  - Nur Manifest
fallback: |
  Bei fehlenden Feldern: Ergänzen
```

```yaml
task: "3.3_create_gateway_mcp_validation"
directory: "units/unified-gateway/"
goal: |
  Erstelle mcp-validation.yml für Gateway mit Public
  Endpoint Checks und Authentication Validation.
tools: |
  - Datei: units/unified-gateway/mcp-validation.yml
  - YAML-Format
  - Gateway-spezifische Checks
work: |
  400 Token (Validation-Config)
negative_constraints: |
  - KEINE Bridge-spezifischen Tests
  - KEINE Implementierung
  - KEINE komplexen Auth-Checks
validation: |
  Negative Constraints:
  - Kein Bridge-Code
  - Keine Test-Logic
  Positive Constraints:
  - Check: public-endpoint Port 8080
  - Check: bearer-auth Required
  - Check: service-discovery Enabled
  - Check: aggregation-support True
  - Check: rate-limiting Configured
  GUTWILLIG:
  - Gateway-Validation
  INTELLIGENT:
  - Gateway-Pattern Checks
  KONTEXT-AWARE:
  - Public Access validiert
  FAUL:
  - Nur Config
fallback: |
  Bei Unsicherheit: Basis-Checks
```

```yaml
task: "3.4_create_gateway_environment"
directory: "units/unified-gateway/config/"
goal: |
  Erstelle env.default mit Gateway-spezifischen Variablen
  für API-Keys, Backend-URLs und Rate-Limits.
tools: |
  - Datei: units/unified-gateway/config/env.default
  - Key=Value Format
  - Gateway-Config
work: |
  300 Token (Environment-Config)
negative_constraints: |
  - KEINE echten API-Keys
  - KEINE festen Service-URLs
  - KEINE Production-Secrets
validation: |
  Negative Constraints:
  - Keine Secrets
  - Keine Hardcoded URLs
  Positive Constraints:
  - GATEWAY_PORT=8080
  - API_KEY=changeme
  - BRIDGE_URL=http://lm-studio-bridge:3000
  - RATE_LIMIT_PER_MINUTE=60
  - LOG_LEVEL=INFO
  - AUTH_ENABLED=true
  GUTWILLIG:
  - Konfigurierbare Gateway
  INTELLIGENT:
  - Service-Discovery ready
  KONTEXT-AWARE:
  - Container-Networking
  FAUL:
  - Nur Config
fallback: |
  Bei fehlenden Vars: Standards
```

```yaml
task: "3.5_create_gateway_dependencies"
directory: "units/unified-gateway/"
goal: |
  Erstelle requirements.txt für Gateway mit MCP SDK first,
  FastMCP und Gateway-spezifischen Dependencies.
tools: |
  - Datei: units/unified-gateway/requirements.txt
  - MCP SDK als erste Zeile
  - Gateway-Packages
work: |
  200 Token (Dependencies)
negative_constraints: |
  - FastMCP NICHT vor MCP SDK
  - KEINE Bridge-Dependencies
  - KEINE Heavy Frameworks
validation: |
  Negative Constraints:
  - MCP SDK first
  - Keine Bridge-Imports
  Positive Constraints:
  - mcp>=1.0.0 (ERSTE ZEILE!)
  - fastmcp>=2.0.0 (ZWEITE ZEILE!)
  - httpx>=0.25.0
  - pydantic>=2.0.0
  - uvicorn>=0.24.0
  - python-multipart>=0.0.6
  GUTWILLIG:
  - Gateway Dependencies
  INTELLIGENT:
  - Minimal für Gateway
  KONTEXT-AWARE:
  - Auth-Support included
  FAUL:
  - Standard Packages
fallback: |
  Bei Unsicherheit: Wie Bridge
```

```yaml
task: "3.6_implement_gateway_server"
directory: "units/unified-gateway/api/"
goal: |
  Implementiere FastMCP Gateway Server mit MCP SDK Base,
  Public Endpoint Configuration und Auth Middleware.
tools: |
  - Datei: units/unified-gateway/api/gateway_server.py
  - MCP SDK + FastMCP
  - Bearer Auth Pattern
work: |
  700 Token (Gateway-Server)
negative_constraints: |
  - KEINE Business-Logic
  - KEINE direkten Service-Calls
  - KEINE Custom Auth
validation: |
  Negative Constraints:
  - Kein Service-Code
  - Keine eigene Auth-Impl
  Positive Constraints:
  - from mcp.server import Server (FIRST!)
  - from fastmcp import FastMCP
  - mcp = FastMCP("unified-gateway")
  - Bearer Token Middleware
  - Public Routes definiert
  - CORS für Browser-Access
  GUTWILLIG:
  - Public MCP Gateway
  INTELLIGENT:
  - Standard Auth-Pattern
  KONTEXT-AWARE:
  - Gateway-Role
  FAUL:
  - Nur Gateway-Setup
fallback: |
  Bei Komplexität: Basic Auth only
```

```yaml
task: "3.7_implement_service_discovery"
directory: "units/unified-gateway/logic/"
goal: |
  Erstelle Service Discovery Client der Bridge-Services
  findet und deren Tools in Registry pflegt.
tools: |
  - Datei: units/unified-gateway/logic/discovery_client.py
  - httpx für Service-Calls
  - asyncio für Periodic Updates
work: |
  600 Token (Discovery-Client)
negative_constraints: |
  - KEINE Service-Implementation
  - KEIN State-Storage
  - KEINE Manual Config
validation: |
  Negative Constraints:
  - Kein Service-Code
  - Kein Persistent State
  Positive Constraints:
  - Connect zu Bridge via BRIDGE_URL
  - GET /mcp/tools periodisch
  - In-Memory Service-Registry
  - Health-Check Integration
  - Auto-Remove bei Failure
  GUTWILLIG:
  - Auto Service-Discovery
  INTELLIGENT:
  - Health-Based Registry
  KONTEXT-AWARE:
  - MCP Tool Discovery
  FAUL:
  - Nur Discovery
fallback: |
  Bei Connection-Error: Empty Registry
```

```yaml
task: "3.8_implement_request_router"
directory: "units/unified-gateway/logic/"
goal: |
  Implementiere Request Router der Tool-Calls zu richtigen
  Backend-Services weiterleitet mit Load-Balancing.
tools: |
  - Datei: units/unified-gateway/logic/router.py
  - Service-Registry Zugriff
  - httpx für Forwarding
work: |
  700 Token (Request-Router)
negative_constraints: |
  - KEINE Request-Modification
  - KEINE Response-Caching
  - KEIN Complex Routing
validation: |
  Negative Constraints:
  - Kein Request-Change
  - Kein Caching
  Positive Constraints:
  - Tool-Name zu Service Mapping
  - Round-Robin Load-Balancing
  - Fallback bei Service-Ausfall
  - Request-Forwarding mit Headers
  - Error-Aggregation
  GUTWILLIG:
  - Transparentes Routing
  INTELLIGENT:
  - Simple Load-Balance
  KONTEXT-AWARE:
  - MCP Tool Pattern
  FAUL:
  - Nur Routing
fallback: |
  Bei Multi-Service: First Available
```

```yaml
task: "3.9_implement_auth_layer"
directory: "units/unified-gateway/api/"
goal: |
  Erstelle Authentication Layer mit Bearer Token Validation
  und Environment-basierten API-Keys.
tools: |
  - Datei: units/unified-gateway/api/auth.py
  - FastAPI Dependencies
  - Environment Config
work: |
  500 Token (Auth-Layer)
negative_constraints: |
  - KEINE User-Datenbank
  - KEINE OAuth/JWT
  - KEIN Session-Management
validation: |
  Negative Constraints:
  - Keine DB-Connection
  - Keine Complex Auth
  Positive Constraints:
  - Bearer Token aus Header
  - Vergleich mit API_KEY env
  - 401 bei Invalid Token
  - Optional via AUTH_ENABLED
  - Rate-Limit per Token
  GUTWILLIG:
  - Basic Security
  INTELLIGENT:
  - Simple Token-Check
  KONTEXT-AWARE:
  - Container-Env
  FAUL:
  - Minimal Auth
fallback: |
  Bei Fehler: Auth disabled
```

```yaml
task: "3.10_implement_response_aggregator"
directory: "units/unified-gateway/logic/"
goal: |
  Implementiere Response Aggregator für Multi-Service
  Responses mit Error Consolidation.
tools: |
  - Datei: units/unified-gateway/logic/aggregator.py
  - Async Response Collection
  - MCP Response Format
work: |
  600 Token (Response-Aggregator)
negative_constraints: |
  - KEINE Response-Transformation
  - KEINE Result-Merging
  - KEIN Buffering
validation: |
  Negative Constraints:
  - Kein Content-Change
  - Kein Response-Cache
  Positive Constraints:
  - Parallel Service-Calls
  - First Success Response
  - Error-Array bei Failures
  - Timeout-Handling (30s)
  - MCP-Format preserved
  GUTWILLIG:
  - Multi-Service Support
  INTELLIGENT:
  - Fast-Return Pattern
  KONTEXT-AWARE:
  - MCP Response Rules
  FAUL:
  - Nur Aggregation
fallback: |
  Bei Multi-Error: First Error
```

```yaml
task: "3.11_create_gateway_dockerfile"
directory: "units/unified-gateway/"
goal: |
  Erstelle Dockerfile für Gateway analog zu Bridge mit
  gleicher Optimierung und Security-Settings.
tools: |
  - Datei: units/unified-gateway/Dockerfile
  - Multi-Stage Pattern
  - Non-Root User
work: |
  500 Token (Dockerfile)
negative_constraints: |
  - KEINE Root-Execution
  - KEINE Dev-Tools
  - KEINE Bridge-Code
validation: |
  Negative Constraints:
  - Kein Root User
  - Keine Build-Tools
  Positive Constraints:
  - FROM python:3.11-alpine
  - Multi-Stage Build
  - USER 1000:1000
  - EXPOSE 8080
  - Health-Check CMD
  - Minimal Size
  GUTWILLIG:
  - Secure Gateway
  INTELLIGENT:
  - Reuse Bridge-Pattern
  KONTEXT-AWARE:
  - Public Port 8080
  FAUL:
  - Copy Bridge-Style
fallback: |
  Bei Error: Single-Stage
```

```yaml
task: "3.12_create_gateway_start_script"
directory: "units/unified-gateway/"
goal: |
  Erstelle start.sh für Gateway mit Dependency-Check
  auf Bridge-Service Health.
tools: |
  - Datei: units/unified-gateway/start.sh
  - Shell-Script
  - Health-Wait Logic
work: |
  400 Token (Start-Script)
negative_constraints: |
  - KEINE infinite Loops
  - KEINE Complex Checks
  - KEIN Service-Management
validation: |
  Negative Constraints:
  - Keine Forever-Loops
  - Kein Complex Logic
  Positive Constraints:
  - #!/bin/sh
  - Wait for Bridge Health (max 60s)
  - Export Python-Path
  - Start Gateway Server
  - Graceful Shutdown
  - Executable Mode
  GUTWILLIG:
  - Reliable Start
  INTELLIGENT:
  - Health-Check Wait
  KONTEXT-AWARE:
  - Service Dependencies
  FAUL:
  - Simple Script
fallback: |
  Bei Wait-Fail: Start anyway
```

```yaml
task: "3.13_create_gateway_health_endpoint"
directory: "units/unified-gateway/api/"
goal: |
  Implementiere Health-Endpoint der Service-Status
  aggregiert und Overall-Health reported.
tools: |
  - Datei: units/unified-gateway/api/health.py
  - Integration in gateway_server.py
  - Service-Registry Access
work: |
  400 Token (Health-Endpoint)
negative_constraints: |
  - KEINE Detail-Logs
  - KEINE Sensitive Info
  - KEIN Heavy Processing
validation: |
  Negative Constraints:
  - Keine Secrets
  - Keine Heavy Checks
  Positive Constraints:
  - GET /health Endpoint
  - Status: healthy/unhealthy
  - Service-Count
  - Last-Check Timestamp
  - 200 OK bei Success
  GUTWILLIG:
  - Monitoring-Ready
  INTELLIGENT:
  - Simple JSON
  KONTEXT-AWARE:
  - Container Health
  FAUL:
  - Basic Status
fallback: |
  Bei Error: Static OK
```

```yaml
task: "3.14_test_gateway_build"
directory: "units/unified-gateway/"
goal: |
  Erstelle test-build.sh für Gateway Container Build
  und Basic Smoke-Test ohne Dependencies.
tools: |
  - Datei: units/unified-gateway/test-build.sh
  - Docker Commands
  - Port-Check
work: |
  300 Token (Test-Script)
negative_constraints: |
  - KEINE Bridge Required
  - KEINE Network Tests
  - KEIN Production Test
validation: |
  Negative Constraints:
  - Keine External Deps
  - Keine Integration
  Positive Constraints:
  - docker build -t gateway:test .
  - docker run --rm -p 8080:8080 gateway:test
  - curl localhost:8080/health
  - Exit-Code Checks
  - Clean-Up
  GUTWILLIG:
  - Quick Test
  INTELLIGENT:
  - Health-Check only
  KONTEXT-AWARE:
  - Port 8080
  FAUL:
  - Minimal Test
fallback: |
  Bei Port-Conflict: Skip
```

```yaml
task: "3.15_update_compose_services"
directory: "ops/compose/"
goal: |
  Erweitere docker-compose.yml um Service-Definitionen
  für Bridge und Gateway mit korrekten Dependencies.
tools: |
  - Update: ops/compose/docker-compose.yml
  - Service-Definitions
  - Health-Checks
work: |
  600 Token (Compose-Update)
negative_constraints: |
  - KEINE host Network
  - KEINE Root-Mounts
  - KEINE Fixed IPs
validation: |
  Negative Constraints:
  - Keine Host-Mode
  - Keine Root-Volumes
  Positive Constraints:
  - lm-studio-bridge Service
  - unified-gateway Service
  - depends_on mit Conditions
  - Health-Check Commands
  - Bridge-Network Usage
  - Restart: unless-stopped
  GUTWILLIG:
  - Complete Stack
  INTELLIGENT:
  - Health-Dependencies
  KONTEXT-AWARE:
  - Service-Order
  FAUL:
  - Two Services
fallback: |
  Bei Syntax-Error: Minimal Version
```

**Phase 3 vollständig definiert. Bestätigung für Phase 4 (Integration & Deployment) erforderlich.**

```yaml
task: "4.1_finalize_docker_compose"
directory: "ops/compose/"
goal: |
  Finalisiere docker-compose.yml mit vollständigen Service-
  Definitionen, Build-Contexts und Environment-Variables.
tools: |
  - Update: ops/compose/docker-compose.yml
  - Docker Compose v3.8
  - Environment substitution
work: |
  700 Token (Complete Compose)
negative_constraints: |
  - KEINE hardcoded Passwords
  - KEINE absolute Paths
  - KEINE host Volumes
  - KEINE privileged Mode
validation: |
  Negative Constraints:
  - Keine Secrets in File
  - Keine Host-Dependencies
  Positive Constraints:
  - Bridge Service mit build Context ../../units/lm-studio-bridge
  - Gateway Service mit build Context ../../units/unified-gateway
  - Environment aus .env File
  - Container Names definiert
  - Labels für Management
  GUTWILLIG:
  - Production-Ready Stack
  INTELLIGENT:
  - Build-Context Paths
  KONTEXT-AWARE:
  - Windows-Compatible
  FAUL:
  - Standard Compose
fallback: |
  Bei Path-Issues: Relative Paths
```

```yaml
task: "4.2_configure_compose_network"
directory: "ops/compose/"
goal: |
  Definiere Bridge-Network in docker-compose.yml mit
  korrekter Isolation und DNS-Resolution.
tools: |
  - In docker-compose.yml
  - Network-Section
  - Driver: bridge
work: |
  300 Token (Network Config)
negative_constraints: |
  - KEINE host Network
  - KEINE macvlan
  - KEINE custom Subnets
  - KEINE external Networks
validation: |
  Negative Constraints:
  - Kein Host-Mode
  - Keine IP-Ranges
  Positive Constraints:
  - networks: llm-hub-net: driver: bridge
  - Alle Services im gleichen Network
  - Automatische DNS-Resolution
  - Internal Communication only
  GUTWILLIG:
  - Isolated Network
  INTELLIGENT:
  - Default Bridge
  KONTEXT-AWARE:
  - Docker Desktop
  FAUL:
  - Simple Network
fallback: |
  Bei Error: Default Network
```

```yaml
task: "4.3_implement_health_checks"
directory: "ops/compose/"
goal: |
  Füge Health-Check Definitionen zu beiden Services
  mit sinnvollen Intervallen und Retry-Counts hinzu.
tools: |
  - In docker-compose.yml
  - healthcheck Sections
  - curl Commands
work: |
  400 Token (Health Checks)
negative_constraints: |
  - KEINE external Tools
  - KEINE komplexen Scripts
  - KEINE langen Timeouts
validation: |
  Negative Constraints:
  - Keine Extra Tools
  - Keine Scripts
  Positive Constraints:
  - Bridge: test: ["CMD", "wget", "-q", "--spider", "http://localhost:3000/health"]
  - Gateway: test: ["CMD", "wget", "-q", "--spider", "http://localhost:8080/health"]
  - interval: 30s, timeout: 10s, retries: 3
  - start_period: 40s
  GUTWILLIG:
  - Reliable Health
  INTELLIGENT:
  - wget statt curl (Alpine)
  KONTEXT-AWARE:
  - Container Ports
  FAUL:
  - Simple Checks
fallback: |
  Bei wget-Fehler: nc -z
```

```yaml
task: "4.4_define_service_dependencies"
directory: "ops/compose/"
goal: |
  Konfiguriere depends_on mit Health-Conditions damit
  Gateway erst nach healthy Bridge startet.
tools: |
  - In docker-compose.yml
  - depends_on with conditions
  - Service order
work: |
  300 Token (Dependencies)
negative_constraints: |
  - KEINE zirkulären Deps
  - KEINE Multi-Level Deps
  - KEINE external Deps
validation: |
  Negative Constraints:
  - Keine Circular Deps
  - Keine Complex Chains
  Positive Constraints:
  - Gateway depends_on: lm-studio-bridge: condition: service_healthy
  - Restart policies: unless-stopped
  - Korrekte Start-Reihenfolge
  GUTWILLIG:
  - Ordered Startup
  INTELLIGENT:
  - Health-Based Wait
  KONTEXT-AWARE:
  - Service Relations
  FAUL:
  - One Dependency
fallback: |
  Bei Version-Issue: Simple depends_on
```

```yaml
task: "4.5_create_env_example"
directory: "ops/compose/"
goal: |
  Erstelle .env.example mit allen Required Environment
  Variables und sinnvollen Default-Werten.
tools: |
  - Datei: ops/compose/.env.example
  - Key=Value Format
  - Dokumentierte Werte
work: |
  400 Token (Environment Template)
negative_constraints: |
  - KEINE echten Secrets
  - KEINE Production URLs
  - KEINE User-spezifische Paths
validation: |
  Negative Constraints:
  - Keine Real Values
  - Keine Secrets
  Positive Constraints:
  - LM_STUDIO_URL=http://host.docker.internal:1234
  - GATEWAY_PORT=8080
  - API_KEY=your-api-key-here
  - LOG_LEVEL=INFO
  - POLL_INTERVAL=30
  - Alle Vars dokumentiert
  GUTWILLIG:
  - Template für User
  INTELLIGENT:
  - Sensible Defaults
  KONTEXT-AWARE:
  - Windows Docker
  FAUL:
  - Only Required Vars
fallback: |
  Bei Missing: Add Standard
```

```yaml
task: "4.6_create_windows_start_script"
directory: "/"
goal: |
  Erstelle start.bat für Windows mit Docker Desktop Check,
  Port-Verfügbarkeit und Compose-Start.
tools: |
  - Datei: start.bat
  - Windows Batch Commands
  - Docker CLI
work: |
  600 Token (Batch Script)
negative_constraints: |
  - KEINE PowerShell
  - KEINE Admin-Rights
  - KEINE GUI-Tools
  - KEINE Loops
validation: |
  Negative Constraints:
  - Kein PowerShell
  - Keine Admin Required
  Positive Constraints:
  - @echo off
  - Check Docker Desktop läuft
  - Check Ports 8080 frei
  - Copy .env.example zu .env wenn fehlt
  - docker-compose up -d
  - Warte auf Health
  - Success-Message mit URLs
  GUTWILLIG:
  - One-Click Start
  INTELLIGENT:
  - Pre-Flight Checks
  KONTEXT-AWARE:
  - Windows Batch
  FAUL:
  - Simple Commands
fallback: |
  Bei Check-Fail: Warning only
```

```yaml
task: "4.7_implement_docker_check"
directory: "/"
goal: |
  Erweitere start.bat um robusten Docker Desktop Check
  mit klarer Fehlermeldung bei fehlendem Docker.
tools: |
  - In start.bat
  - docker version Command
  - Error Messages
work: |
  300 Token (Docker Check)
negative_constraints: |
  - KEINE Installation
  - KEINE Registry Login
  - KEINE Updates
validation: |
  Negative Constraints:
  - Kein Auto-Install
  - Keine Downloads
  Positive Constraints:
  - docker version >nul 2>&1
  - IF ERRORLEVEL 1 mit Message
  - Link zu Docker Desktop Download
  - Exit bei Fehler
  - Clear Error Text
  GUTWILLIG:
  - User Guidance
  INTELLIGENT:
  - Simple Check
  KONTEXT-AWARE:
  - Windows Docker
  FAUL:
  - Version Check only
fallback: |
  Bei Complex: Just docker ps
```

```yaml
task: "4.8_implement_port_check"
directory: "/"
goal: |
  Füge Port-Verfügbarkeits-Check zu start.bat hinzu
  für Port 8080 mit Hinweis bei Konflikt.
tools: |
  - In start.bat
  - netstat Command
  - findstr for Port
work: |
  300 Token (Port Check)
negative_constraints: |
  - KEINE Port-Kills
  - KEINE Service-Stops
  - KEINE Admin-Commands
validation: |
  Negative Constraints:
  - Kein Process Kill
  - Keine Force-Free
  Positive Constraints:
  - netstat -an | findstr :8080
  - Check LISTENING State
  - Warning wenn belegt
  - Vorschlag anderen Port
  - Continue möglich
  GUTWILLIG:
  - Prevent Conflicts
  INTELLIGENT:
  - Non-Invasive
  KONTEXT-AWARE:
  - Common Port
  FAUL:
  - Check only
fallback: |
  Bei netstat-Fail: Skip Check
```

```yaml
task: "4.9_implement_compose_start"
directory: "/"
goal: |
  Implementiere Docker Compose Start-Sequenz in start.bat
  mit Verzeichniswechsel und Status-Output.
tools: |
  - In start.bat
  - cd Command
  - docker-compose up
work: |
  400 Token (Compose Start)
negative_constraints: |
  - KEINE Build-Force
  - KEINE Recreate-Always
  - KEINE Foreground-Mode
validation: |
  Negative Constraints:
  - Kein --force-recreate
  - Kein Foreground
  Positive Constraints:
  - cd ops\compose
  - docker-compose up -d
  - Echo Starting Services
  - Show Container Status
  - Return zu Root-Dir
  GUTWILLIG:
  - Clean Start
  INTELLIGENT:
  - Detached Mode
  KONTEXT-AWARE:
  - Relative Paths
  FAUL:
  - Standard up -d
fallback: |
  Bei Path-Issue: Full Path
```

```yaml
task: "4.10_implement_health_wait"
directory: "/"
goal: |
  Füge Health-Check Wait-Loop zu start.bat hinzu
  der auf beide Services wartet mit Timeout.
tools: |
  - In start.bat
  - timeout Command
  - docker inspect
work: |
  500 Token (Health Wait)
negative_constraints: |
  - KEINE infinite Loops
  - KEINE langen Waits
  - KEINE komplexen Checks
validation: |
  Negative Constraints:
  - Keine Forever-Loop
  - Max 60s Wait
  Positive Constraints:
  - Loop mit Counter (max 12)
  - docker inspect für Health
  - 5 Sekunden zwischen Checks
  - Break bei beiden healthy
  - Timeout Message
  GUTWILLIG:
  - Reliable Startup
  INTELLIGENT:
  - Timeout Protection
  KONTEXT-AWARE:
  - Two Services
  FAUL:
  - Simple Loop
fallback: |
  Bei Complex: Fixed 30s wait
```

```yaml
task: "4.11_create_success_output"
directory: "/"
goal: |
  Erstelle Success-Message in start.bat mit URLs
  und Next-Steps für User.
tools: |
  - In start.bat
  - echo Commands
  - ASCII Banner optional
work: |
  300 Token (Success Message)
negative_constraints: |
  - KEINE Colors/ANSI
  - KEINE externen Tools
  - KEINE GUI
validation: |
  Negative Constraints:
  - Keine Fancy Output
  - Keine External Tools
  Positive Constraints:
  - Clear Success Banner
  - Gateway URL: http://localhost:8080
  - LM Studio URL: http://localhost:1234
  - Health-Check: http://localhost:8080/health
  - Next Steps Info
  GUTWILLIG:
  - User Friendly
  INTELLIGENT:
  - All URLs listed
  KONTEXT-AWARE:
  - Local URLs
  FAUL:
  - Text only
fallback: |
  Bei Error: Simple Done
```

```yaml
task: "4.12_implement_error_handling"
directory: "/"
goal: |
  Füge Error-Handling zu start.bat mit klaren Messages
  und Troubleshooting-Hints hinzu.
tools: |
  - In start.bat
  - Error-Checks
  - Help Messages
work: |
  400 Token (Error Handling)
negative_constraints: |
  - KEINE Logs löschen
  - KEINE Auto-Fixes
  - KEINE Diagnose-Tools
validation: |
  Negative Constraints:
  - Keine Auto-Repair
  - Keine Log-Deletion
  Positive Constraints:
  - Check docker-compose Exit-Code
  - Error-Message bei Fail
  - Hint: Check Logs
  - Hint: Port Conflicts
  - Hint: Docker Desktop
  GUTWILLIG:
  - Helpful Errors
  INTELLIGENT:
  - Common Issues
  KONTEXT-AWARE:
  - Windows Problems
  FAUL:
  - Messages only
fallback: |
  Bei Complex: Generic Error
```

```yaml
task: "4.13_create_stop_script"
directory: "/"
goal: |
  Erstelle stop.bat für sauberes Herunterfahren
  aller Services mit Graceful Shutdown.
tools: |
  - Datei: stop.bat
  - docker-compose down
  - Status Messages
work: |
  300 Token (Stop Script)
negative_constraints: |
  - KEINE Volume-Löschung
  - KEINE Image-Removal
  - KEINE Force-Kill
validation: |
  Negative Constraints:
  - Keine Data Loss
  - Keine Image Delete
  Positive Constraints:
  - @echo off
  - cd ops\compose
  - docker-compose down
  - Show Shutdown Status
  - Success Message
  - Return to Root
  GUTWILLIG:
  - Clean Shutdown
  INTELLIGENT:
  - Preserve Data
  KONTEXT-AWARE:
  - Graceful Stop
  FAUL:
  - Simple down
fallback: |
  Bei Error: Continue
```

```yaml
task: "4.14_create_logs_script"
directory: "/"
goal: |
  Erstelle logs.bat zum Anzeigen der Container-Logs
  beider Services für Debugging.
tools: |
  - Datei: logs.bat
  - docker-compose logs
  - tail/follow Option
work: |
  200 Token (Logs Script)
negative_constraints: |
  - KEINE Log-Files
  - KEINE Filtering
  - KEINE Parsing
validation: |
  Negative Constraints:
  - Keine File-Output
  - Keine Processing
  Positive Constraints:
  - @echo off
  - cd ops\compose
  - docker-compose logs -f --tail=100
  - Info about Ctrl+C
  - Both Services
  GUTWILLIG:
  - Debug Support
  INTELLIGENT:
  - Follow Mode
  KONTEXT-AWARE:
  - Container Logs
  FAUL:
  - Standard logs
fallback: |
  Bei Error: docker logs
```

```yaml
task: "4.15_finalize_environment_setup"
directory: "ops/compose/"
goal: |
  Erstelle finale Environment-Setup-Dokumentation
  in .env.example mit ausführlichen Kommentaren.
tools: |
  - Update: ops/compose/.env.example
  - Inline Documentation
  - Section Headers
work: |
  400 Token (Env Documentation)
negative_constraints: |
  - KEINE Code-Examples
  - KEINE Scripts
  - KEINE Secrets
validation: |
  Negative Constraints:
  - Keine Executable
  - Keine Real Keys
  Positive Constraints:
  - Section: LM Studio Config
  - Section: Gateway Config
  - Section: Logging Config
  - Jede Variable dokumentiert
  - Beispiel-Werte sinnvoll
  - Copy-Paste ready
  GUTWILLIG:
  - Self-Documenting
  INTELLIGENT:
  - Grouped Sections
  KONTEXT-AWARE:
  - All Services
  FAUL:
  - Comments only
fallback: |
  Bei Length: Reduce Comments
```

