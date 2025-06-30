```yaml
task: "5.1_create_integration_test_setup"
directory: "ops/scripts/"
goal: |
  Erstelle integration-test.sh Script das System-Start
  mit LM Studio Mock testet und Health-Checks prüft.
tools: |
  - Datei: ops/scripts/integration-test.sh
  - Docker Commands
  - Health-Check Verification
work: |
  500 Token (Test Setup)
negative_constraints: |
  - KEIN echter LM Studio
  - KEINE Production-Data
  - KEINE externen Services
  - KEINE Cleanup von User-Data
validation: |
  Negative Constraints:
  - Kein LM Studio Required
  - Keine Real Models
  Positive Constraints:
  - Mock LM Studio mit Python http.server
  - docker-compose up -d
  - Wait for Health-Checks
  - Verify beide Services healthy
  - Exit-Code 0 bei Success
  GUTWILLIG:
  - Automated Testing
  INTELLIGENT:
  - Mock statt Real
  KONTEXT-AWARE:
  - Container Testing
  FAUL:
  - Basic Checks
fallback: |
  Bei Mock-Fail: Skip Test
```

```yaml
task: "5.2_implement_lm_studio_mock"
directory: "ops/scripts/"
goal: |
  Erstelle lm-studio-mock.py der LM Studio HTTP API
  simuliert mit /v1/models und /v1/completions.
tools: |
  - Datei: ops/scripts/lm-studio-mock.py
  - Python http.server
  - JSON Responses
work: |
  600 Token (Mock Server)
negative_constraints: |
  - KEINE echte Inference
  - KEINE Model-Files
  - KEINE GPU-Usage
  - KEINE komplexe Logic
validation: |
  Negative Constraints:
  - Keine Real Models
  - Keine Processing
  Positive Constraints:
  - GET /v1/models returns 2 fake models
  - POST /v1/completions returns static response
  - Streaming SSE Support
  - Port 1234 Binding
  - CORS Headers
  GUTWILLIG:
  - Testable API
  INTELLIGENT:
  - Minimal Mock
  KONTEXT-AWARE:
  - OpenAI Format
  FAUL:
  - Static Responses
fallback: |
  Bei Complex: Simple JSON
```

```yaml
task: "5.3_test_service_discovery"
directory: "ops/scripts/"
goal: |
  Erweitere integration-test.sh um Discovery-Test
  der prüft ob Models als MCP-Tools erscheinen.
tools: |
  - In integration-test.sh
  - curl Commands
  - jq for JSON parsing
work: |
  400 Token (Discovery Test)
negative_constraints: |
  - KEINE Installation von Tools
  - KEINE komplexen Parsings
  - KEINE langen Waits
validation: |
  Negative Constraints:
  - Keine Extra Tools
  - Keine Complex Logic
  Positive Constraints:
  - Wait 35 Sekunden (Poll-Interval)
  - GET localhost:8080/mcp/tools
  - Check 2 Tools vorhanden
  - Verify Tool-Namen match Models
  - Clear Test Output
  GUTWILLIG:
  - Discovery Validation
  INTELLIGENT:
  - Simple JSON Check
  KONTEXT-AWARE:
  - 30s Poll Cycle
  FAUL:
  - Basic Verification
fallback: |
  Bei jq-Missing: grep
```

```yaml
task: "5.4_test_gateway_health"
directory: "ops/scripts/"
goal: |
  Implementiere Health-Endpoint-Test für Gateway
  der Service-Status und Aggregation prüft.
tools: |
  - In integration-test.sh
  - curl localhost:8080/health
  - Status-Code Check
work: |
  300 Token (Health Test)
negative_constraints: |
  - KEINE Detail-Analyse
  - KEINE Performance-Tests
  - KEINE Load-Tests
validation: |
  Negative Constraints:
  - Keine Deep Checks
  - Keine Benchmarks
  Positive Constraints:
  - GET /health returns 200
  - JSON contains status: healthy
  - services Array nicht leer
  - timestamp vorhanden
  - Echo Test Result
  GUTWILLIG:
  - Health Verification
  INTELLIGENT:
  - HTTP Code Check
  KONTEXT-AWARE:
  - Gateway Port 8080
  FAUL:
  - Simple GET
fallback: |
  Bei Fail: Retry Once
```

```yaml
task: "5.5_create_inference_test"
directory: "ops/scripts/"
goal: |
  Erstelle inference-test.py der MCP Tool-Call
  über Gateway testet mit Mock-Response-Verify.
tools: |
  - Datei: ops/scripts/inference-test.py
  - httpx für API Calls
  - MCP Protocol Format
work: |
  600 Token (Inference Test)
negative_constraints: |
  - KEINE echte AI-Response
  - KEINE Model-Evaluation
  - KEINE Performance-Messung
validation: |
  Negative Constraints:
  - Keine Real Inference
  - Keine Benchmarking
  Positive Constraints:
  - POST /mcp/tools/{name}/call
  - MCP-konformer Request
  - Bearer Token aus ENV
  - Response-Validation
  - Exit 0 bei Success
  GUTWILLIG:
  - E2E Validation
  INTELLIGENT:
  - Mock-Aware Test
  KONTEXT-AWARE:
  - MCP Protocol
  FAUL:
  - Single Request
fallback: |
  Bei Protocol-Error: Skip
```

```yaml
task: "5.6_test_streaming_response"
directory: "ops/scripts/"
goal: |
  Erweitere inference-test.py um Streaming-Response-Test
  mit SSE-Event-Parsing und Chunk-Validation.
tools: |
  - In inference-test.py
  - SSE Client Code
  - Async Streaming
work: |
  500 Token (Streaming Test)
negative_constraints: |
  - KEINE Buffer-Overflows
  - KEINE Memory-Leaks
  - KEINE Infinite Streams
validation: |
  Negative Constraints:
  - Keine Memory Issues
  - Keine Endless Loops
  Positive Constraints:
  - Stream-Parameter in Request
  - SSE Events empfangen
  - Chunks validieren
  - Proper Stream Close
  - Success-Message
  GUTWILLIG:
  - Streaming Verify
  INTELLIGENT:
  - Async Handling
  KONTEXT-AWARE:
  - SSE Format
  FAUL:
  - Basic Stream
fallback: |
  Bei SSE-Fail: Non-Stream Test
```

```yaml
task: "5.7_test_error_handling"
directory: "ops/scripts/"
goal: |
  Erstelle error-test.py der verschiedene Fehler-Szenarien
  testet wie ungültige Models und Auth-Fehler.
tools: |
  - Datei: ops/scripts/error-test.py
  - Invalid Requests
  - Error-Response Checks
work: |
  400 Token (Error Tests)
negative_constraints: |
  - KEINE Crash-Tests
  - KEINE DOS-Attacks
  - KEINE System-Overload
validation: |
  Negative Constraints:
  - Keine Destructive Tests
  - Keine Overload
  Positive Constraints:
  - Invalid Model Name → 404
  - Missing Auth → 401
  - Invalid JSON → 400
  - Error-Format validieren
  - Graceful Failures
  GUTWILLIG:
  - Robustness Check
  INTELLIGENT:
  - Common Errors
  KONTEXT-AWARE:
  - MCP Errors
  FAUL:
  - Few Scenarios
fallback: |
  Bei Crash: Mark Failed
```

```yaml
task: "5.8_create_direct_access_test"
directory: "ops/scripts/"
goal: |
  Erstelle direct-test.py der direkten LM Studio Zugriff
  testet um beide Access-Modes zu verifizieren.
tools: |
  - Datei: ops/scripts/direct-test.py
  - Direct Port 1234
  - OpenAI Client Format
work: |
  400 Token (Direct Test)
negative_constraints: |
  - KEINE MCP-Usage hier
  - KEINE Gateway-Calls
  - KEINE Auth Required
validation: |
  Negative Constraints:
  - Kein Gateway Test
  - Kein MCP Format
  Positive Constraints:
  - GET localhost:1234/v1/models
  - POST localhost:1234/v1/completions
  - OpenAI-Format Request
  - Response-Validation
  - Compare mit Gateway-Response
  GUTWILLIG:
  - Dual-Mode Test
  INTELLIGENT:
  - Direct Compare
  KONTEXT-AWARE:
  - Port 1234
  FAUL:
  - Two Calls
fallback: |
  Bei Port-Closed: Skip
```

```yaml
task: "5.9_implement_performance_check"
directory: "ops/scripts/"
goal: |
  Erweitere Tests um Basic Performance-Check der
  First-Token-Latency unter 100ms verifiziert.
tools: |
  - In inference-test.py
  - time Measurements
  - Latency Calculation
work: |
  300 Token (Performance Check)
negative_constraints: |
  - KEINE Load-Tests
  - KEINE Stress-Tests
  - KEINE Parallel-Requests
validation: |
  Negative Constraints:
  - Keine Heavy Load
  - Keine Concurrency
  Positive Constraints:
  - Measure Request Start
  - Measure First Chunk
  - Calculate Latency
  - Warn if > 100ms
  - Info Output Only
  GUTWILLIG:
  - Performance Info
  INTELLIGENT:
  - Single Measure
  KONTEXT-AWARE:
  - Local Network
  FAUL:
  - One Timing
fallback: |
  Bei Timer-Issue: Skip
```

```yaml
task: "5.10_create_test_runner"
directory: "ops/scripts/"
goal: |
  Erstelle run-all-tests.sh der alle Test-Scripts
  sequenziell ausführt mit Summary-Report.
tools: |
  - Datei: ops/scripts/run-all-tests.sh
  - Shell Script
  - Test Execution
work: |
  400 Token (Test Runner)
negative_constraints: |
  - KEINE Parallel-Tests
  - KEINE Test-Dependencies
  - KEINE Cleanup
validation: |
  Negative Constraints:
  - Keine Parallel Run
  - Keine Interdependencies
  Positive Constraints:
  - Start Mock Server
  - Run integration-test.sh
  - Run Python Tests
  - Collect Exit-Codes
  - Summary mit Pass/Fail
  - Stop Mock Server
  GUTWILLIG:
  - Test Automation
  INTELLIGENT:
  - Sequential Run
  KONTEXT-AWARE:
  - All Test Types
  FAUL:
  - Simple Runner
fallback: |
  Bei Script-Fail: Continue
```

```yaml
task: "5.11_document_test_results"
directory: "ops/scripts/"
goal: |
  Erstelle test-results-template.md für dokumentierte
  Test-Durchläufe mit Checklist-Format.
tools: |
  - Datei: ops/scripts/test-results-template.md
  - Markdown Format
  - Checklist Items
work: |
  300 Token (Test Template)
negative_constraints: |
  - KEINE Automation
  - KEINE Scripts
  - KEINE Tools
validation: |
  Negative Constraints:
  - Keine Executable
  - Keine Automation
  Positive Constraints:
  - Test-Date Field
  - Checklist für jeden Test
  - Expected vs Actual
  - Pass/Fail Checkboxes
  - Notes-Section
  GUTWILLIG:
  - Test Tracking
  INTELLIGENT:
  - Simple Checklist
  KONTEXT-AWARE:
  - All Test-Cases
  FAUL:
  - Static Template
fallback: |
  Bei Format: Plain Text
```

```yaml
task: "5.12_create_troubleshooting_guide"
directory: "docs/"
goal: |
  Erstelle TROUBLESHOOTING.md mit häufigen Problemen
  und Lösungen für Docker und Service-Issues.
tools: |
  - Datei: docs/TROUBLESHOOTING.md
  - Problem-Solution Format
  - Windows-Focus
work: |
  500 Token (Troubleshooting)
negative_constraints: |
  - KEINE Code-Fixes
  - KEINE Scripts
  - KEINE Admin-Commands
validation: |
  Negative Constraints:
  - Keine Executable
  - Keine Sudo/Admin
  Positive Constraints:
  - Port 8080 belegt → Lösung
  - Docker nicht läuft → Lösung
  - Service unhealthy → Logs prüfen
  - Connection refused → Firewall
  - Common Windows Issues
  GUTWILLIG:
  - User Support
  INTELLIGENT:
  - Common Problems
  KONTEXT-AWARE:
  - Windows/Docker
  FAUL:
  - Text Guide
fallback: |
  Bei Length: Top 5 Issues
```

```yaml
task: "5.13_test_model_updates"
directory: "ops/scripts/"
goal: |
  Erstelle model-update-test.py der dynamisches Model-
  Hinzufügen und Entfernen zur Laufzeit testet.
tools: |
  - Datei: ops/scripts/model-update-test.py
  - Mock-Server Manipulation
  - Poll-Cycle Wait
work: |
  500 Token (Update Test)
negative_constraints: |
  - KEINE Service-Restarts
  - KEINE Container-Rebuilds
  - KEINE Config-Changes
validation: |
  Negative Constraints:
  - Keine Restart Required
  - Keine Rebuilds
  Positive Constraints:
  - Add Model zu Mock
  - Wait 35 Sekunden
  - Verify New Tool appears
  - Remove Model
  - Verify Tool removed
  GUTWILLIG:
  - Dynamic Updates
  INTELLIGENT:
  - Runtime Changes
  KONTEXT-AWARE:
  - Discovery Cycle
  FAUL:
  - Add/Remove Only
fallback: |
  Bei Timing: Increase Wait
```

```yaml
task: "5.14_validate_mcp_compliance"
directory: "ops/scripts/"
goal: |
  Nutze mcp-validate.py um beide Units auf vollständige
  MCP-Compliance zu prüfen mit allen Endpoints.
tools: |
  - Run: ops/scripts/mcp-validate.py
  - Für beide Units
  - Full Validation
work: |
  400 Token (MCP Validation)
negative_constraints: |
  - KEINE Code-Änderungen
  - KEINE Fixes
  - KEINE Partial-Checks
validation: |
  Negative Constraints:
  - Keine Modifications
  - Keine Skips
  Positive Constraints:
  - Run für lm-studio-bridge
  - Run für unified-gateway
  - Check alle MCP-Endpoints
  - Verify Lifecycle-Support
  - Exit 0 für beide
  GUTWILLIG:
  - Spec Compliance
  INTELLIGENT:
  - Use Existing Tool
  KONTEXT-AWARE:
  - MCP 2025-06-18
  FAUL:
  - Run Validator
fallback: |
  Bei Tool-Missing: Manual Check
```

```yaml
task: "5.15_create_test_summary"
directory: "ops/scripts/"
goal: |
  Erstelle test-summary.sh das alle Test-Ergebnisse
  sammelt und übersichtlichen Report generiert.
tools: |
  - Datei: ops/scripts/test-summary.sh
  - Parse Test-Outputs
  - Summary Table
work: |
  400 Token (Summary Script)
negative_constraints: |
  - KEINE HTML-Reports
  - KEINE External Tools
  - KEINE Uploads
validation: |
  Negative Constraints:
  - Keine Web-Reports
  - Keine Cloud
  Positive Constraints:
  - ASCII Table Format
  - Test-Name | Status | Time
  - Total Pass/Fail Count
  - Overall Status
  - Save zu test-report.txt
  GUTWILLIG:
  - Clear Results
  INTELLIGENT:
  - Simple Table
  KONTEXT-AWARE:
  - All Tests
  FAUL:
  - Text Output
fallback: |
  Bei Parse-Fail: List Format
```

**Phase 5 vollständig definiert. Bestätigung für Phase 6 (Documentation & Polish) erforderlich.**

```yaml
task: "6.1_create_main_readme"
directory: "/"
goal: |
  Erweitere README.md mit vollständiger Projekt-Übersicht,
  Quick-Start-Guide und Links zu weiterer Dokumentation.
tools: |
  - Update: README.md
  - Markdown Format
  - Keine Code-Examples
work: |
  600 Token (Main README)
negative_constraints: |
  - KEINE Code-Snippets
  - KEINE technischen Details
  - KEINE Konfiguration
  - KEINE langen Texte
validation: |
  Negative Constraints:
  - Kein Code
  - Keine Config-Details
  Positive Constraints:
  - Projekt-Titel und Beschreibung
  - Features-Liste (Bullet Points)
  - Quick Start: 1. LM Studio 2. start.bat
  - Links zu docs/
  - Prerequisites-Section
  - Max 50 Zeilen
  GUTWILLIG:
  - User-Friendly Intro
  INTELLIGENT:
  - Links statt Details
  KONTEXT-AWARE:
  - Windows-Focus
  FAUL:
  - Overview Only
fallback: |
  Bei zu lang: Kürzen
```

```yaml
task: "6.2_create_architecture_overview"
directory: "docs/architecture/"
goal: |
  Erstelle OVERVIEW.md mit System-Architektur-Beschreibung
  inkl. ASCII-Diagrammen und Komponenten-Erklärung.
tools: |
  - Datei: docs/architecture/OVERVIEW.md
  - ASCII Diagrams
  - Component Descriptions
work: |
  700 Token (Architecture Doc)
negative_constraints: |
  - KEINE Implementation-Details
  - KEINE Code-Examples
  - KEINE Config-Snippets
validation: |
  Negative Constraints:
  - Kein Source-Code
  - Keine Configs
  Positive Constraints:
  - System-Übersicht ASCII-Art
  - Komponenten: LM Studio, Bridge, Gateway
  - Datenfluss-Diagramm
  - Port-Mappings Tabelle
  - MCP-Protocol Erwähnung
  GUTWILLIG:
  - Technical Overview
  INTELLIGENT:
  - Visual Diagrams
  KONTEXT-AWARE:
  - Docker Architecture
  FAUL:
  - High-Level Only
fallback: |
  Bei ASCII-Complex: Vereinfachen
```

```yaml
task: "6.3_create_installation_guide"
directory: "docs/"
goal: |
  Erstelle INSTALL.md mit detaillierter Schritt-für-Schritt
  Installationsanleitung für Windows-User.
tools: |
  - Datei: docs/INSTALL.md
  - Numbered Steps
  - Screenshots Placeholders
work: |
  500 Token (Install Guide)
negative_constraints: |
  - KEINE Admin-Rechte
  - KEINE komplexen Setups
  - KEINE Alternativ-OS
validation: |
  Negative Constraints:
  - Keine Root/Admin
  - Keine Linux/Mac
  Positive Constraints:
  - Prerequisites mit Links
  - Docker Desktop Installation
  - LM Studio Setup
  - Repository Clone
  - start.bat Ausführung
  - Verification Steps
  GUTWILLIG:
  - Beginner-Friendly
  INTELLIGENT:
  - Clear Steps
  KONTEXT-AWARE:
  - Windows 11
  FAUL:
  - Windows Only
fallback: |
  Bei Details: Link zu Docs
```

```yaml
task: "6.4_create_configuration_guide"
directory: "docs/"
goal: |
  Erstelle CONFIGURATION.md mit Erklärung aller
  Environment-Variablen und Anpassungsmöglichkeiten.
tools: |
  - Datei: docs/CONFIGURATION.md
  - Table Format
  - Examples
work: |
  600 Token (Config Guide)
negative_constraints: |
  - KEINE Secrets
  - KEINE Debug-Configs
  - KEINE Experimental
validation: |
  Negative Constraints:
  - Keine API-Keys
  - Keine Debug-Modes
  Positive Constraints:
  - Tabelle: Variable | Default | Beschreibung
  - Sections für jeden Service
  - Beispiel .env File
  - Common Anpassungen
  - Performance-Tuning Basics
  GUTWILLIG:
  - Config Reference
  INTELLIGENT:
  - Structured Tables
  KONTEXT-AWARE:
  - Service-Specific
  FAUL:
  - Standard Configs
fallback: |
  Bei Länge: Nur Required
```

```yaml
task: "6.5_create_api_documentation"
directory: "docs/api/"
goal: |
  Erstelle MCP-ENDPOINTS.md mit Dokumentation aller
  verfügbaren MCP-Endpoints und Request/Response-Beispielen.
tools: |
  - Datei: docs/api/MCP-ENDPOINTS.md
  - Endpoint-Liste
  - JSON Examples
work: |
  700 Token (API Docs)
negative_constraints: |
  - KEINE Implementation
  - KEINE internen Endpoints
  - KEINE Debug-APIs
validation: |
  Negative Constraints:
  - Kein Code
  - Keine Internals
  Positive Constraints:
  - GET /health
  - GET /mcp/tools
  - POST /mcp/tools/{name}/call
  - Request/Response Examples
  - Status-Codes
  - Auth-Requirements
  GUTWILLIG:
  - API Reference
  INTELLIGENT:
  - Clear Examples
  KONTEXT-AWARE:
  - MCP Standard
  FAUL:
  - Public APIs Only
fallback: |
  Bei Complex: Core Endpoints
```

```yaml
task: "6.6_create_development_guide"
directory: "docs/"
goal: |
  Erstelle DEVELOPMENT.md für Entwickler die neue
  Features hinzufügen oder Units erweitern möchten.
tools: |
  - Datei: docs/DEVELOPMENT.md
  - dedardf-Rules
  - Unit-Structure
work: |
  600 Token (Dev Guide)
negative_constraints: |
  - KEINE Code-Generation
  - KEINE Tool-Empfehlungen
  - KEINE IDE-Configs
validation: |
  Negative Constraints:
  - Keine Generators
  - Keine IDE-Setup
  Positive Constraints:
  - dedardf-Struktur erklärt
  - Neue Unit hinzufügen Steps
  - Contract-Definition Guide
  - Testing-Approach
  - PR-Guidelines
  GUTWILLIG:
  - Developer Docs
  INTELLIGENT:
  - Process-Focus
  KONTEXT-AWARE:
  - dedardf Method
  FAUL:
  - Structure Only
fallback: |
  Bei Length: Link zu dedardf
```

```yaml
task: "6.7_update_adr_index"
directory: "docs/architecture/decisions/"
goal: |
  Erstelle ADR-INDEX.md mit Übersicht aller Architecture
  Decision Records und deren Status.
tools: |
  - Datei: docs/architecture/decisions/ADR-INDEX.md
  - Table Format
  - Links zu ADRs
work: |
  300 Token (ADR Index)
negative_constraints: |
  - KEINE neuen ADRs
  - KEINE Details
  - KEINE Diskussion
validation: |
  Negative Constraints:
  - Keine ADR-Inhalte
  - Keine Bewertung
  Positive Constraints:
  - Tabelle: ADR# | Title | Status | Date
  - ADR-001: Minimal Platform
  - ADR-002: HTTP-Only Bridge
  - Links zu Files
  - Template-Verweis
  GUTWILLIG:
  - ADR Overview
  INTELLIGENT:
  - Simple Index
  KONTEXT-AWARE:
  - Existing ADRs
  FAUL:
  - Index Only
fallback: |
  Bei Missing: List Format
```

```yaml
task: "6.8_create_changelog"
directory: "/"
goal: |
  Erstelle CHANGELOG.md mit Initial Release 1.0.0
  Entry und Standard-Format für Updates.
tools: |
  - Datei: CHANGELOG.md
  - Keep-a-Changelog Format
  - Semantic Versioning
work: |
  300 Token (Changelog)
negative_constraints: |
  - KEINE Future-Releases
  - KEINE Roadmap
  - KEINE Promises
validation: |
  Negative Constraints:
  - Keine Unreleased
  - Keine Roadmap
  Positive Constraints:
  - ## [1.0.0] - 2025-01-30
  - ### Added Section
  - Initial Features Liste
  - Link zu README
  - Standard Format
  GUTWILLIG:
  - Version History
  INTELLIGENT:
  - Standard Format
  KONTEXT-AWARE:
  - Initial Release
  FAUL:
  - One Version
fallback: |
  Bei Format: Simple List
```

```yaml
task: "6.9_create_license_file"
directory: "/"
goal: |
  Erstelle LICENSE Datei mit MIT License für
  Open-Source-Nutzung des Projekts.
tools: |
  - Datei: LICENSE
  - MIT License Text
  - Copyright 2025
work: |
  200 Token (License)
negative_constraints: |
  - KEINE Custom-License
  - KEINE Modifications
  - KEINE Zusätze
validation: |
  Negative Constraints:
  - Keine Änderungen
  - Keine Extras
  Positive Constraints:
  - Standard MIT License
  - Copyright 2025
  - Project Name: LLM Hub
  - Full License Text
  - Keine Anpassungen
  GUTWILLIG:
  - Open Source
  INTELLIGENT:
  - Standard MIT
  KONTEXT-AWARE:
  - Current Year
  FAUL:
  - Copy-Paste
fallback: |
  Bei Unsicher: MIT Template
```

```yaml
task: "6.10_create_docker_ignore"
directory: "/"
goal: |
  Erstelle .dockerignore Files für beide Units um
  Build-Context zu minimieren und Secrets auszuschließen.
tools: |
  - units/lm-studio-bridge/.dockerignore
  - units/unified-gateway/.dockerignore
  - Standard Patterns
work: |
  300 Token (Docker Ignores)
negative_constraints: |
  - KEINE Source-Excludes
  - KEINE Required Files
  - KEINE Wildcards
validation: |
  Negative Constraints:
  - Keine *.py Excludes
  - Keine Overly Broad
  Positive Constraints:
  - __pycache__/
  - *.pyc
  - .env
  - .git/
  - tests/
  - *.log
  GUTWILLIG:
  - Smaller Images
  INTELLIGENT:
  - Standard Patterns
  KONTEXT-AWARE:
  - Python Project
  FAUL:
  - Common Ignores
fallback: |
  Bei Unsicher: Minimal Set
```

```yaml
task: "6.11_optimize_container_startup"
directory: "units/"
goal: |
  Optimiere start.sh Scripts beider Units für schnelleren
  Startup und bessere Error-Messages.
tools: |
  - Update: lm-studio-bridge/start.sh
  - Update: unified-gateway/start.sh
  - Shell Optimizations
work: |
  400 Token (Startup Optimize)
negative_constraints: |
  - KEINE Parallelisierung
  - KEINE Hintergrund-Jobs
  - KEINE Komplexität
validation: |
  Negative Constraints:
  - Keine Background
  - Keine Parallel
  Positive Constraints:
  - set -e für Fail-Fast
  - Echo Status-Messages
  - Trap für Cleanup
  - Clear Error bei Env-Missing
  - Schneller Python-Import
  GUTWILLIG:
  - Faster Startup
  INTELLIGENT:
  - Error Handling
  KONTEXT-AWARE:
  - Alpine Shell
  FAUL:
  - Simple Changes
fallback: |
  Bei Complex: Revert
```

```yaml
task: "6.12_add_container_labels"
directory: "ops/compose/"
goal: |
  Füge Docker Labels zu Services in docker-compose.yml
  für besseres Container-Management und Monitoring.
tools: |
  - Update: docker-compose.yml
  - Label Definitions
  - Standard Labels
work: |
  300 Token (Container Labels)
negative_constraints: |
  - KEINE Custom-Schemas
  - KEINE Secrets
  - KEINE URLs
validation: |
  Negative Constraints:
  - Keine Secrets
  - Keine Personal Info
  Positive Constraints:
  - org.label-schema.name
  - org.label-schema.version
  - org.label-schema.description
  - com.llm-hub.service-type
  - com.llm-hub.mcp-enabled
  GUTWILLIG:
  - Better Management
  INTELLIGENT:
  - Standard Schema
  KONTEXT-AWARE:
  - Service Types
  FAUL:
  - Basic Labels
fallback: |
  Bei Schema: Skip Labels
```

```yaml
task: "6.13_create_release_checklist"
directory: "docs/"
goal: |
  Erstelle RELEASE-CHECKLIST.md mit Schritten für
  neue Releases und Deployment-Vorbereitung.
tools: |
  - Datei: docs/RELEASE-CHECKLIST.md
  - Checklist Format
  - Release Steps
work: |
  400 Token (Release List)
negative_constraints: |
  - KEINE Automation
  - KEINE CI/CD
  - KEINE Uploads
validation: |
  Negative Constraints:
  - Keine Scripts
  - Keine Auto-Deploy
  Positive Constraints:
  - [ ] Version Bump
  - [ ] CHANGELOG Update
  - [ ] Run All Tests
  - [ ] Build Containers
  - [ ] Tag Git Release
  - [ ] Update README
  GUTWILLIG:
  - Release Process
  INTELLIGENT:
  - Manual Checklist
  KONTEXT-AWARE:
  - Local Deploy
  FAUL:
  - Simple List
fallback: |
  Bei Complex: Basic Steps
```

```yaml
task: "6.14_final_validation_run"
directory: "/"
goal: |
  Führe finale Validierung aller Scripts und Configs
  durch mit rule0-check.sh und Test-Summary.
tools: |
  - Run: ops/scripts/rule0-check.sh
  - Run: ops/scripts/run-all-tests.sh
  - Verify Results
work: |
  300 Token (Final Check)
negative_constraints: |
  - KEINE Code-Fixes
  - KEINE Änderungen
  - KEINE Workarounds
validation: |
  Negative Constraints:
  - Keine Modifications
  - Keine Patches
  Positive Constraints:
  - rule0-check Exit 0
  - Alle Tests PASS
  - Document Results
  - Create VALIDATION.md
  - Timestamp Results
  GUTWILLIG:
  - Quality Check
  INTELLIGENT:
  - Use Existing
  KONTEXT-AWARE:
  - All Validators
  FAUL:
  - Run Only
fallback: |
  Bei Fail: Document Issue
```

```yaml
task: "6.15_create_success_banner"
directory: "/"
goal: |
  Erstelle SUCCESS.txt mit ASCII-Art Banner für
  erfolgreichen System-Start als Motivations-Boost.
tools: |
  - Datei: SUCCESS.txt
  - ASCII Art
  - Success Message
work: |
  200 Token (Success Banner)
negative_constraints: |
  - KEINE Farben
  - KEINE Unicode
  - KEINE Huge Art
validation: |
  Negative Constraints:
  - Keine ANSI Codes
  - Keine Special Chars
  Positive Constraints:
  - LLM HUB ASCII Logo
  - Success Message
  - Version 1.0.0
  - Ready to Use!
  - Max 10 Zeilen
  GUTWILLIG:
  - User Delight
  INTELLIGENT:
  - Simple ASCII
  KONTEXT-AWARE:
  - Project Name
  FAUL:
  - Static File
fallback: |
  Bei ASCII-Fail: Text Only
```

```yaml
task: "6.16_create_professional_readme"
directory: "/"
goal: |
  Create professional README.md based on NEOMINT template
  for LLM Hub with clear structure and consistent English.
tools: |
  - Replace: README.md
  - NEOMINT Template Format
  - Professional English
work: |
  800 Token (Professional README)
negative_constraints: |
  - NO emojis or casual language
  - NO marketing speech
  - NO code examples
  - NO German text
validation: |
  Negative Constraints:
  - No emojis anywhere
  - No informal language
  Positive Constraints:
  - Title: LLM Hub - Zero-Configuration MCP Bridge
  - Badges: Docker, MCP, Windows, CC BY-NC 4.0
  - Sections: Overview, Quick Launch, Structure, Core, Modules
  - Copyright © 2025 NEOMINT-RESEARCH
  - Author: SKR
  - Consistent English
  GUTWILLIG:
  - Professional documentation
  INTELLIGENT:
  - Template adaptation
  KONTEXT-AWARE:
  - LLM Hub specific
  FAUL:
  - Template structure only
fallback: |
  If uncertain: Follow template exactly
```

```yaml
task: "6.17_create_cc_license"
directory: "/"
goal: |
  Create LICENSE file with Creative Commons BY-NC 4.0
  according to NEOMINT standard for non-commercial use.
tools: |
  - Replace: LICENSE
  - CC BY-NC 4.0 full text
  - NEOMINT copyright header
work: |
  300 Token (CC License)
negative_constraints: |
  - NO modifications to license text
  - NO additional terms
  - NO commercial permissions
validation: |
  Negative Constraints:
  - No license modifications
  - No extra clauses
  Positive Constraints:
  - Full CC BY-NC 4.0 text
  - Copyright (c) 2025 NEOMINT-RESEARCH
  - Author: SKR
  - Contact: research@neomint.com
  - Link to legal code
  GUTWILLIG:
  - Clear licensing
  INTELLIGENT:
  - Standard CC text
  KONTEXT-AWARE:
  - Non-commercial
  FAUL:
  - Exact copy
fallback: |
  If doubt: Use template exactly
```

```yaml
task: "6.18_create_contributing_guide"
directory: "/"
goal: |
  Create CONTRIBUTING.md following NEOMINT template with
  clear contribution process in professional English.
tools: |
  - Create: CONTRIBUTING.md
  - NEOMINT contribution format
  - Git workflow steps
work: |
  500 Token (Contributing Guide)
negative_constraints: |
  - NO complex processes
  - NO tool requirements
  - NO German text
validation: |
  Negative Constraints:
  - No mandatory tools
  - No complex workflows
  Positive Constraints:
  - Fork and branch process
  - dedardf structure compliance
  - Validation script reference
  - Legal notice section
  - Contact: research@neomint.com
  - Professional English
  GUTWILLIG:
  - Clear contribution path
  INTELLIGENT:
  - Standard Git flow
  KONTEXT-AWARE:
  - dedardf compliance
  FAUL:
  - Template based
fallback: |
  If complex: Simplify to basics
```

```yaml
task: "6.19_create_opensource_doc"
directory: "/"
goal: |
  Create OPEN_SOURCE.md with usage philosophy and
  commercial licensing info per NEOMINT standard.
tools: |
  - Create: OPEN_SOURCE.md
  - NEOMINT philosophy text
  - Usage permissions
work: |
  600 Token (Open Source Doc)
negative_constraints: |
  - NO commercial permissions
  - NO warranty claims
  - NO German text
validation: |
  Negative Constraints:
  - No commercial use allowed
  - No guarantees
  Positive Constraints:
  - Project: LLM Hub
  - Copyright © 2025 NEOMINT-RESEARCH
  - Philosophy section
  - Permitted/Restricted uses
  - Commercial licensing contact
  - Professional tone
  GUTWILLIG:
  - Clear usage terms
  INTELLIGENT:
  - NEOMINT philosophy
  KONTEXT-AWARE:
  - Research context
  FAUL:
  - Template structure
fallback: |
  If unsure: Copy template style
```

```yaml
task: "6.20_update_all_docs_english"
directory: "docs/"
goal: |
  Update all documentation files to consistent English
  with professional tone and unified style.
tools: |
  - Update: All .md files in docs/
  - English translation
  - Style consistency
work: |
  800 Token (Doc Updates)
negative_constraints: |
  - NO German remains
  - NO mixed languages
  - NO casual tone
  - NO emojis
validation: |
  Negative Constraints:
  - No German text anywhere
  - No language mixing
  Positive Constraints:
  - INSTALL.md → English
  - CONFIGURATION.md → English
  - TROUBLESHOOTING.md → English
  - DEVELOPMENT.md → English
  - Consistent terminology
  - Professional tone throughout
  GUTWILLIG:
  - Unified documentation
  INTELLIGENT:
  - Consistent style
  KONTEXT-AWARE:
  - Technical accuracy
  FAUL:
  - Translation only
fallback: |
  If term unclear: Use standard tech English
```

```yaml
task: "6.21_update_architecture_docs"
directory: "docs/architecture/"
goal: |
  Ensure all architecture documentation uses consistent
  English terminology and NEOMINT professional style.
tools: |
  - Update: OVERVIEW.md
  - Update: decisions/*.md
  - Professional English
work: |
  600 Token (Architecture Docs)
negative_constraints: |
  - NO German technical terms
  - NO informal explanations
  - NO inconsistent naming
validation: |
  Negative Constraints:
  - No German remains
  - No casual language
  Positive Constraints:
  - OVERVIEW.md in English
  - ADR-001/002 in English
  - Consistent component names
  - Professional diagrams
  - Clear technical language
  GUTWILLIG:
  - Professional architecture docs
  INTELLIGENT:
  - Technical precision
  KONTEXT-AWARE:
  - System architecture
  FAUL:
  - Language update only
fallback: |
  If technical term unclear: Use industry standard
```

```yaml
task: "6.22_create_validation_report"
directory: "docs/"
goal: |
  Create VALIDATION.md with final system validation
  results in English with timestamp and checklist.
tools: |
  - Create: docs/VALIDATION.md
  - Validation results format
  - Professional report style
work: |
  400 Token (Validation Report)
negative_constraints: |
  - NO test implementation
  - NO German text
  - NO informal notes
validation: |
  Negative Constraints:
  - No code or scripts
  - No casual comments
  Positive Constraints:
  - Validation Date: 2025-01-30
  - dedardf Compliance: PASSED
  - MCP Validation: PASSED
  - Integration Tests: PASSED
  - Professional format
  - NEOMINT header
  GUTWILLIG:
  - Quality documentation
  INTELLIGENT:
  - Clear results
  KONTEXT-AWARE:
  - All test types
  FAUL:
  - Report only
fallback: |
  If results unclear: Mark as pending
```

**STATUS: COMPLETED**

```yaml
task: "6.23_update_scripts_comments"
directory: "/"
goal: |
  Update all script comments and messages to English
  for consistency across the entire project.
tools: |
  - Update: start.bat echo messages
  - Update: stop.bat messages
  - Update: All .sh/.py comments
work: |
  500 Token (Script Updates)
negative_constraints: |
  - NO German in scripts
  - NO mixed languages
  - NO emoji in output
validation: |
  Negative Constraints:
  - No German anywhere
  - No informal messages
  Positive Constraints:
  - start.bat messages in English
  - Error messages in English
  - Comments in English
  - Professional tone
  - Clear instructions
  GUTWILLIG:
  - Consistent UX
  INTELLIGENT:
  - User-friendly English
  KONTEXT-AWARE:
  - Windows users
  FAUL:
  - Text updates only
fallback: |
  If phrase unclear: Use simple English
```

**STATUS: COMPLETED** (All scripts already in English)

```yaml
task: "6.24_create_project_metadata"
directory: "/"
goal: |
  Create .project.json with NEOMINT-compliant metadata
  for project identification and versioning.
tools: |
  - Create: .project.json
  - NEOMINT metadata format
  - Project information
work: |
  300 Token (Project Metadata)
negative_constraints: |
  - NO personal information
  - NO internal URLs
  - NO German text
validation: |
  Negative Constraints:
  - No private data
  - No internal refs
  Positive Constraints:
  - name: "llm-hub"
  - version: "1.0.0"
  - description: English
  - author: "SKR"
  - organization: "NEOMINT-RESEARCH"
  - license: "CC-BY-NC-4.0"
  GUTWILLIG:
  - Machine-readable info
  INTELLIGENT:
  - Standard format
  KONTEXT-AWARE:
  - Project specific
  FAUL:
  - Metadata only
fallback: |
  If field unclear: Omit it
```

**STATUS: COMPLETED**

```yaml
task: "6.25_final_consistency_check"
directory: "/"
goal: |
  Perform final consistency check ensuring all documentation,
  code comments, and user messages are in professional English.
tools: |
  - grep for German words
  - Check all .md files
  - Verify consistency
work: |
  400 Token (Consistency Check)
negative_constraints: |
  - NO changes to code logic
  - NO file deletions
  - NO structural changes
validation: |
  Negative Constraints:
  - No code modifications
  - No file removal
  Positive Constraints:
  - All docs in English
  - Consistent terminology
  - Professional tone
  - NEOMINT compliance
  - Create LANGUAGE-CHECK.md report
  GUTWILLIG:
  - Quality assurance
  INTELLIGENT:
  - Automated checks
  KONTEXT-AWARE:
  - Full project
  FAUL:
  - Check only
fallback: |
  If issues found: Document in report
```

**STATUS: COMPLETED** (All files verified in English, report created)
