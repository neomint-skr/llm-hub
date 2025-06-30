# Phase 1: Foundation & Validation (30 Min)

## Subtask 1.1: Repository Setup

```yaml
task: "1.1_create_repository_structure"
directory: "/"
goal: |
  Erstelle die vollständige dedardf-konforme Verzeichnisstruktur 
  für das LLM Hub Projekt mit allen erforderlichen Unterverzeichnissen
  und .gitkeep Dateien in leeren Verzeichnissen.
tools: |
  - mkdir für Verzeichniserstellung
  - touch für .gitkeep Dateien
  - Erlaubte Pfade: alle gemäß dedardf-Struktur
work: |
  500 Token (Struktur erstellen und verifizieren)
negative_constraints: |
  - KEINE Dateien außerhalb der definierten Struktur
  - KEINE Business-Logik oder Code
  - KEINE .env oder Makefile im Root
  - KEINE globalen Konfigurationsdateien
validation: |
  Negative Constraints:
  - Keine Dateien außerhalb dedardf-Struktur
  - Keine verbotenen Dateitypen (Makefile, .env)
  Positive Constraints:
  - Vollständige Struktur: platform/, units/, shared/, ops/, docs/, .config/
  - Alle Unterverzeichnisse gemäß Architektur-Diagramm
  - .gitkeep in allen leeren Verzeichnissen
  GUTWILLIG:
  - Saubere Basis für weitere Entwicklung
  INTELLIGENT:
  - Minimale Struktur, keine überflüssigen Verzeichnisse
  KONTEXT-AWARE:
  - Exakte Übereinstimmung mit dedardf-Methodik
  FAUL:
  - Nur Verzeichnisse, keine Inhalte
fallback: |
  Bei fehlenden Verzeichnissen: Struktur vervollständigen
  Bei falschen Pfaden: Korrigieren gemäß dedardf
```

## Subtask 1.2: Git & Tooling Setup

```yaml
task: "1.2_configure_git_and_tooling"
directory: "/"
goal: |
  Erstelle Git-Konfigurationsdateien (.gitignore, .gitattributes)
  und Python-Linting-Konfiguration für das Projekt.
tools: |
  - Datei-Erstellung: .gitignore, .gitattributes
  - Verzeichnis: .config/
  - Datei: .config/linter.yml
work: |
  300 Token (Templates erstellen)
negative_constraints: |
  - KEINE projektspezifischen Ignores außer Standard Python
  - KEINE komplexen Linter-Regeln
  - KEINE IDE-spezifischen Konfigurationen
validation: |
  Negative Constraints:
  - Keine überflüssigen Konfigurationen
  Positive Constraints:
  - .gitignore mit Python-Standards (__pycache__, *.pyc, .env, *.log, .venv/)
  - .gitattributes für Windows/Linux Line-Endings
  - .config/linter.yml mit Basis Python-Linting
  GUTWILLIG:
  - Verhindert Commit von generierten Dateien
  INTELLIGENT:
  - Minimale, aber vollständige Konfiguration
  KONTEXT-AWARE:
  - Windows-kompatible Line-Endings beachtet
  FAUL:
  - Nur definierte Dateien erstellt
fallback: |
  Bei fehlenden Einträgen: Standard-Templates verwenden
```

## Subtask 1.3: Root Documentation

```yaml
task: "1.3_create_root_documentation"
directory: "/"
goal: |
  Erstelle minimales README.md mit Projekttitel und 
  Verweis auf Architektur-Dokumentation.
tools: |
  - Datei: README.md
  - Keine Code-Beispiele erlaubt
work: |
  200 Token (Kurzes README)
negative_constraints: |
  - KEINE Code-Beispiele
  - KEINE Installationsanleitungen
  - KEINE technischen Details
  - KEIN Marketing-Text
validation: |
  Negative Constraints:
  - Kein Code im README
  - Keine technische Dokumentation
  Positive Constraints:
  - Titel: "LLM Hub - Zero-Configuration MCP Bridge"
  - Verweis auf docs/architecture/
  - Maximal 10 Zeilen
  GUTWILLIG:
  - Klarer Einstiegspunkt für Entwickler
  INTELLIGENT:
  - Minimal, verweist auf Details
  KONTEXT-AWARE:
  - Nutzt korrekte Projektbezeichnung
  FAUL:
  - Nur README.md, keine weiteren Docs
fallback: |
  Bei zu langem Text: Auf Essenz reduzieren
```

## Subtask 1.4: Platform Core Implementation

```yaml
task: "1.4_implement_platform_core"
directory: "platform/core/"
goal: |
  Implementiere minimalen Contract-Loader und YAML-Validator
  für die Platform-Core-Komponente ohne Business-Logik.
tools: |
  - Dateien in platform/core/
  - Python mit yaml, pathlib
  - Keine externen Dependencies
work: |
  800 Token (Contract-Loader + Validator)
negative_constraints: |
  - KEINE Business-Logik
  - KEINE Unit-spezifischen Features
  - KEINE komplexen Validierungen
  - KEINE externen Libraries außer yaml
validation: |
  Negative Constraints:
  - Keine Business-Logik vorhanden
  - Keine Unit-Abhängigkeiten
  Positive Constraints:
  - contract_loader.py lädt .yml aus platform/contracts/
  - Basis-YAML-Validierung (Syntax, nicht Schema)
  - Fehlerbehandlung für fehlende/fehlerhafte Dateien
  GUTWILLIG:
  - Stabile Basis für Contract-System
  INTELLIGENT:
  - Minimale Implementierung, erweiterbar
  KONTEXT-AWARE:
  - Folgt dedardf Contract-Konzept
  FAUL:
  - Nur Loader, keine Interpretation
fallback: |
  Bei Komplexität: Auf reines Laden reduzieren
```

## Subtask 1.5: Platform Runtime Bootstrap

```yaml
task: "1.5_create_runtime_bootstrap"
directory: "platform/runtime/"
goal: |
  Erstelle Bootstrap-Modul mit JSON-Logging-Setup,
  Environment-Variable-Validator und gemeinsame Error-Handler.
tools: |
  - Dateien in platform/runtime/
  - Python logging, json, os
  - Keine externen Dependencies
work: |
  600 Token (Bootstrap-Components)
negative_constraints: |
  - KEINE Unit-spezifische Logik
  - KEINE komplexen Logging-Frameworks
  - KEINE Datenbank-Logs
validation: |
  Negative Constraints:
  - Keine Unit-Dependencies
  - Kein externes Logging-Framework
  Positive Constraints:
  - bootstrap.py mit init_logging() für JSON-Format
  - env_validator.py prüft Required Variables
  - error_handler.py mit BaseError-Klassen
  GUTWILLIG:
  - Einheitliche Basis für alle Units
  INTELLIGENT:
  - Wiederverwendbare Komponenten
  KONTEXT-AWARE:
  - JSON-Logs für Container-Umgebung
  FAUL:
  - Nur definierte Module
fallback: |
  Bei Überladung: Features reduzieren
```

## Subtask 1.6: Platform Runtime Lifecycle

```yaml
task: "1.6_implement_lifecycle_management"
directory: "platform/runtime/"
goal: |
  Implementiere MCP-Standard Lifecycle-Phasen, Signal-Handler
  für Graceful Shutdown und Health-Check Aggregator.
tools: |
  - lifecycle.py in platform/runtime/
  - Python signal, asyncio
  - MCP-Spezifikation als Referenz
work: |
  700 Token (Lifecycle-Implementation)
negative_constraints: |
  - KEINE Unit-spezifischen Lifecycle-Events
  - KEINE komplexen State-Machines
  - KEINE persistenten States
validation: |
  Negative Constraints:
  - Kein Unit-spezifischer Code
  - Kein State-Management
  Positive Constraints:
  - MCP Lifecycle-Phasen: startup, ready, shutdown
  - SIGTERM/SIGINT Handler für Graceful Shutdown
  - Health-Check Aggregator sammelt Unit-Status
  GUTWILLIG:
  - Sauberes Shutdown-Verhalten
  INTELLIGENT:
  - Standard-Patterns für Container
  KONTEXT-AWARE:
  - MCP-konforme Phasen
  FAUL:
  - Nur Lifecycle-Management
fallback: |
  Bei Komplexität: Auf Basis-Signale reduzieren
```

## Subtask 1.7: Platform ADR Documentation

```yaml
task: "1.7_create_adr_documentation"
directory: "docs/architecture/decisions/"
goal: |
  Erstelle ADR-001 und ADR-002 für grundlegende Architektur-
  Entscheidungen und ADR-Template für weitere Entscheidungen.
tools: |
  - Markdown-Dateien in docs/architecture/decisions/
  - ADR-Standard-Format
work: |
  500 Token (3 ADR-Dateien)
negative_constraints: |
  - KEINE technischen Implementierungsdetails
  - KEINE Code-Beispiele
  - KEINE zu langen Texte
validation: |
  Negative Constraints:
  - Kein Code in ADRs
  - Keine Implementierungsdetails
  Positive Constraints:
  - ADR-001-minimal-platform.md
  - ADR-002-http-only-bridge.md
  - ADR-000-template.md
  - Standard ADR-Format (Status, Context, Decision, Consequences)
  GUTWILLIG:
  - Dokumentierte Entscheidungen
  INTELLIGENT:
  - Kurz und prägnant
  KONTEXT-AWARE:
  - Bezug auf LLM Hub Kontext
  FAUL:
  - Nur 3 Dateien
fallback: |
  Bei zu viel Text: Auf Kernaussagen reduzieren
```

```yaml
task: "1.8_define_lm_bridge_contract"
directory: "platform/contracts/"
goal: |
  Erstelle vollständigen MCP-Contract für LM-Studio-Bridge Unit
  mit allen erforderlichen Endpoints, Schemas und Events.
tools: |
  - Datei: platform/contracts/lm-bridge.v1.yml
  - YAML-Format
  - MCP-Spezifikation 2025-06-18
work: |
  600 Token (Contract-Definition)
negative_constraints: |
  - KEINE Implementierungsdetails
  - KEINE Unit-spezifische Logik
  - KEINE proprietären Erweiterungen
  - KEINE Breaking Changes erlaubt
validation: |
  Negative Constraints:
  - Kein Code, nur Spezifikation
  - Keine Implementation-Details
  Positive Constraints:
  - Vollständige MCP-Endpoint-Liste (/mcp/context, /mcp/lifecycle, /mcp/tools, /health)
  - Request/Response Schemas für alle Endpoints
  - Lifecycle Requirements definiert
  - Event-Definitionen für Model-Discovery
  GUTWILLIG:
  - Klare Schnittstelle für Bridge-Unit
  INTELLIGENT:
  - Standard MCP-Format verwendet
  KONTEXT-AWARE:
  - LM Studio spezifische Erweiterungen
  FAUL:
  - Nur Contract-Definition
fallback: |
  Bei fehlenden Endpoints: MCP-Spec konsultieren
```

```yaml
task: "1.9_define_gateway_contract"
directory: "platform/contracts/"
goal: |
  Erstelle Gateway-Contract mit Public Endpoint Specs,
  Authentication Schema und Routing Rules.
tools: |
  - Datei: platform/contracts/gateway.v1.yml
  - YAML-Format
  - Bezug auf lm-bridge.v1.yml
work: |
  500 Token (Gateway-Contract)
negative_constraints: |
  - KEINE Duplikation von Bridge-Contract
  - KEINE komplexen Auth-Mechanismen
  - KEINE Business-Logic in Contract
validation: |
  Negative Constraints:
  - Keine Code-Snippets
  - Keine Implementierung
  Positive Constraints:
  - Public Endpoint auf Port 8080 spezifiziert
  - Bearer Token Authentication Schema
  - Routing Rules zu Bridge-Services
  - Consumes: lm-bridge.v1
  GUTWILLIG:
  - Einheitlicher Zugriffspunkt definiert
  INTELLIGENT:
  - Minimale Auth-Anforderungen
  KONTEXT-AWARE:
  - Aggregation mehrerer Bridges vorbereitet
  FAUL:
  - Nur Gateway-spezifische Aspekte
fallback: |
  Bei Überkomplexität: Auf Basis-Routing reduzieren
```

```yaml
task: "1.10_define_discovery_contract"
directory: "platform/contracts/"
goal: |
  Erstelle Discovery-Contract für Service-Registry Format,
  Health-Status Schema und Capability Advertisement.
tools: |
  - Datei: platform/contracts/discovery.v1.yml
  - YAML-Format
  - Event-basierte Updates
work: |
  400 Token (Discovery-Contract)
negative_constraints: |
  - KEINE Implementierung von Discovery
  - KEINE komplexen Protokolle
  - KEINE proprietären Formate
validation: |
  Negative Constraints:
  - Kein Discovery-Code
  - Keine komplexen Mechanismen
  Positive Constraints:
  - Service-Registry Schema (name, version, endpoints)
  - Health-Status Format (status, timestamp, details)
  - Capability Advertisement (models, features)
  - Update-Event Definitionen
  GUTWILLIG:
  - Standardisierte Service-Discovery
  INTELLIGENT:
  - Einfaches Key-Value Format
  KONTEXT-AWARE:
  - Model-Discovery berücksichtigt
  FAUL:
  - Nur Schema-Definitionen
fallback: |
  Bei Komplexität: Auf Basis-Registry reduzieren
```

```yaml
task: "1.11_create_rule0_validator"
directory: "ops/scripts/"
goal: |
  Implementiere Rule0-Checker Script das verbotene Patterns
  scannt und Struktur-Compliance prüft.
tools: |
  - Datei: ops/scripts/rule0-check.sh
  - Bash-Script
  - find, grep Commands
work: |
  400 Token (Validation-Script)
negative_constraints: |
  - KEINE komplexen Regex
  - KEINE externen Tools
  - KEINE Änderungen, nur Prüfung
validation: |
  Negative Constraints:
  - Script ändert nichts
  - Keine externen Dependencies
  Positive Constraints:
  - Prüft auf Makefile/env im Root
  - Scannt verbotene Pfade (tests/, platform/shared/)
  - Findet relative Imports zwischen Units
  - Exit-Code 0 bei Erfolg, 1 bei Fehler
  GUTWILLIG:
  - Automatisierte Compliance-Prüfung
  INTELLIGENT:
  - Einfache Shell-Commands
  KONTEXT-AWARE:
  - dedardf-Regeln implementiert
  FAUL:
  - Nur definierte Checks
fallback: |
  Bei Shell-Problemen: Vereinfachen
```

```yaml
task: "1.12_create_mcp_validator"
directory: "ops/scripts/"
goal: |
  Erstelle MCP-Validator Script für Unit-Manifest Checks,
  Endpoint-Verfügbarkeit und Lifecycle-Support.
tools: |
  - Datei: ops/scripts/mcp-validate.py
  - Python mit yaml, requests
  - Bezug auf mcp-validation.yml
work: |
  600 Token (MCP-Validator)
negative_constraints: |
  - KEINE Unit-spezifischen Tests
  - KEINE komplexen Validierungen
  - KEINE externen Validator-Libs
validation: |
  Negative Constraints:
  - Keine Unit-Logik
  - Keine komplexen Dependencies
  Positive Constraints:
  - Lädt mcp-validation.yml aus Unit
  - Prüft unit.yml Vollständigkeit
  - Testet Endpoint-Erreichbarkeit
  - Validiert Lifecycle-Phasen
  GUTWILLIG:
  - MCP-Compliance sichergestellt
  INTELLIGENT:
  - Wiederverwendbar für alle Units
  KONTEXT-AWARE:
  - MCP 2025-06-18 Spec
  FAUL:
  - Nur MCP-Validation
fallback: |
  Bei Fehler: Basis-Checks implementieren
```

```yaml
task: "1.13_create_docker_compose_base"
directory: "ops/compose/"
goal: |
  Erstelle docker-compose.yml Grundstruktur mit Netzwerk-
  Definition und Platzhaltern für Services.
tools: |
  - Datei: ops/compose/docker-compose.yml
  - Docker Compose v3.8 Format
  - Bridge-Network Definition
work: |
  300 Token (Compose-Grundstruktur)
negative_constraints: |
  - KEINE Service-Definitionen (nur Struktur)
  - KEINE Volumes außer logs
  - KEINE Host-Network
  - KEINE hardcodierten Ports
validation: |
  Negative Constraints:
  - Keine Services definiert
  - Kein Host-Network-Mode
  Positive Constraints:
  - Version: "3.8"
  - Bridge-Network "llm-hub-net" definiert
  - Platzhalter-Kommentare für Services
  - Log-Volume vorbereitet
  GUTWILLIG:
  - Basis für Service-Integration
  INTELLIGENT:
  - Standard Docker-Network
  KONTEXT-AWARE:
  - Windows Docker Desktop kompatibel
  FAUL:
  - Nur Netzwerk-Definition
fallback: |
  Bei Syntax-Fehler: Minimal-Version
```

```yaml
task: "2.1_create_bridge_unit_structure"
directory: "units/lm-studio-bridge/"
goal: |
  Erstelle vollständige Unit-Verzeichnisstruktur für 
  LM-Studio-Bridge mit allen erforderlichen Unterverzeichnissen.
tools: |
  - mkdir für Verzeichnisse
  - touch für Placeholder-Dateien
  - Struktur: api/, logic/, config/, config/mocks/
work: |
  200 Token (Struktur erstellen)
negative_constraints: |
  - KEINE Dateien mit Inhalt
  - KEINE zusätzlichen Verzeichnisse
  - KEINE Cross-Unit-Referenzen
validation: |
  Negative Constraints:
  - Keine Inhalte in Dateien
  - Keine Extra-Verzeichnisse
  Positive Constraints:
  - api/, logic/, config/ Verzeichnisse
  - config/mocks/ für Test-Daten
  - .gitkeep in leeren Verzeichnissen
  GUTWILLIG:
  - Klare Unit-Struktur
  INTELLIGENT:
  - Minimale Verzeichnisse
  KONTEXT-AWARE:
  - dedardf-konforme Unit
  FAUL:
  - Nur Struktur, kein Code
fallback: |
  Bei fehlenden Dirs: Nacherstellen
```

```yaml
task: "2.2_create_unit_manifest"
directory: "units/lm-studio-bridge/"
goal: |
  Erstelle vollständiges unit.yml Manifest mit allen
  Required Fields für die LM-Studio-Bridge Unit.
tools: |
  - Datei: units/lm-studio-bridge/unit.yml
  - YAML-Format
  - MCP-Unit-Type Declaration
work: |
  400 Token (Unit-Manifest)
negative_constraints: |
  - KEINE Implementierungsdetails
  - KEINE ungültigen Contract-Referenzen
  - KEINE fehlenden Pflichtfelder
validation: |
  Negative Constraints:
  - Keine Code-Snippets
  - Keine falschen Referenzen
  Positive Constraints:
  - id: "lm-studio-bridge"
  - version: "1.0.0"
  - type: "mcp-service"
  - contracts: exposes["lm-bridge.v1"], consumes["discovery.v1"]
  - entrypoint: "./start.sh"
  - mcp: true, discovery.enabled: true
  GUTWILLIG:
  - Vollständige Unit-Beschreibung
  INTELLIGENT:
  - Alle Pflichtfelder, keine Extras
  KONTEXT-AWARE:
  - Referenziert Platform-Contracts
  FAUL:
  - Nur Manifest-Definition
fallback: |
  Bei fehlenden Feldern: Ergänzen
```

```yaml
task: "2.3_define_mcp_validation"
directory: "units/lm-studio-bridge/"
goal: |
  Erstelle mcp-validation.yml mit allen erforderlichen
  Checks für MCP-Compliance der Bridge-Unit.
tools: |
  - Datei: units/lm-studio-bridge/mcp-validation.yml
  - YAML-Format
  - MCP 2025-06-18 Spec
work: |
  400 Token (Validation-Config)
negative_constraints: |
  - KEINE Implementierung von Checks
  - KEINE Custom-Validations
  - KEINE nicht-MCP Tests
validation: |
  Negative Constraints:
  - Kein Test-Code
  - Keine Custom-Logic
  Positive Constraints:
  - sdk: "python", spec_version: "2025-06-18"
  - Check: sdk-version >=1.0.0
  - Check: exposes-api für alle MCP-Endpoints
  - Check: lifecycle-support [startup, shutdown, healthcheck]
  - Check: contract-alignment mit lm-bridge.v1
  GUTWILLIG:
  - Automatisierbare Validation
  INTELLIGENT:
  - Standard MCP-Checks
  KONTEXT-AWARE:
  - Bridge-spezifische Endpoints
  FAUL:
  - Nur Validation-Config
fallback: |
  Bei Spec-Unsicherheit: Basis-Checks
```

```yaml
task: "2.4_create_environment_config"
directory: "units/lm-studio-bridge/config/"
goal: |
  Erstelle env.default mit allen Environment-Variablen
  für LM-Studio-Bridge mit sinnvollen Defaults.
tools: |
  - Datei: units/lm-studio-bridge/config/env.default
  - Key=Value Format
  - Kommentare für Dokumentation
work: |
  300 Token (Environment-Config)
negative_constraints: |
  - KEINE Secrets oder Passwörter
  - KEINE hartkodierten IPs
  - KEINE produktiven Werte
validation: |
  Negative Constraints:
  - Keine Secrets
  - Keine festen IPs
  Positive Constraints:
  - LM_STUDIO_URL=http://host.docker.internal:1234
  - MCP_PORT=3000
  - POLL_INTERVAL=30
  - LOG_LEVEL=INFO
  - Alle Werte dokumentiert
  GUTWILLIG:
  - Konfigurierbare Unit
  INTELLIGENT:
  - Sinnvolle Defaults
  KONTEXT-AWARE:
  - host.docker.internal für Windows
  FAUL:
  - Nur Environment-Variablen
fallback: |
  Bei fehlenden Vars: Ergänzen
```

```yaml
task: "2.5_setup_mcp_dependencies"
directory: "units/lm-studio-bridge/"
goal: |
  Erstelle requirements.txt mit MCP SDK als erste Dependency,
  gefolgt von FastMCP und weiteren erforderlichen Paketen.
tools: |
  - Datei: units/lm-studio-bridge/requirements.txt
  - Pip-Format
  - Versionierte Dependencies
work: |
  200 Token (Dependency-Liste)
negative_constraints: |
  - KEINE unveröffentlichten Pakete
  - KEINE Entwickler-Dependencies
  - KEINE GPU-Libraries
  - FastMCP NICHT vor MCP SDK
validation: |
  Negative Constraints:
  - MCP SDK muss ERSTE Zeile sein
  - Keine Dev-Dependencies
  Positive Constraints:
  - mcp>=1.0.0 (ERSTE ZEILE!)
  - fastmcp>=2.0.0 (ZWEITE ZEILE!)
  - httpx>=0.25.0
  - pydantic>=2.0.0
  - uvicorn>=0.24.0
  GUTWILLIG:
  - Korrekte Dependency-Order
  INTELLIGENT:
  - Minimale Dependencies
  KONTEXT-AWARE:
  - MCP SDK vor FastMCP!
  FAUL:
  - Nur Required Packages
fallback: |
  Bei falscher Reihenfolge: MCP SDK first!
```

```yaml
task: "2.6_implement_mcp_server_base"
directory: "units/lm-studio-bridge/api/"
goal: |
  Implementiere MCP-Server Grundgerüst mit FastMCP,
  korrekt aufbauend auf MCP SDK mit Basis-Configuration.
tools: |
  - Datei: units/lm-studio-bridge/api/mcp_server.py
  - Python mit MCP SDK und FastMCP
  - Import from platform.runtime
work: |
  600 Token (Server-Grundgerüst)
negative_constraints: |
  - KEINE Business-Logic
  - KEINE Model-spezifischen Features
  - FastMCP NICHT ohne MCP SDK importieren
validation: |
  Negative Constraints:
  - Kein LM Studio Code
  - Imports in richtiger Reihenfolge
  Positive Constraints:
  - from mcp.server import Server (ZUERST!)
  - from fastmcp import FastMCP (DANACH!)
  - mcp = FastMCP("lm-studio-bridge")
  - Basis-Routes für MCP-Endpoints
  GUTWILLIG:
  - Lauffähiger MCP-Server
  INTELLIGENT:
  - FastMCP für schnelle Impl
  KONTEXT-AWARE:
  - Nutzt platform.runtime.bootstrap
  FAUL:
  - Nur Server-Setup
fallback: |
  Bei Import-Fehler: MCP SDK first!
```

```yaml
task: "2.7_implement_tool_definitions"
directory: "units/lm-studio-bridge/api/"
goal: |
  Definiere MCP-Tools mit FastMCP @mcp.tool() Decorators
  für Model-Inference mit Type-Hints und Docstrings.
tools: |
  - Erweitere: api/mcp_server.py
  - FastMCP Tool-Decorators
  - Pydantic Models für Parameter
work: |
  500 Token (Tool-Definitionen)
negative_constraints: |
  - KEINE Implementierung, nur Stubs
  - KEINE komplexen Parameter
  - KEINE Model-Loading
validation: |
  Negative Constraints:
  - Keine echte Inference-Logic
  - Keine Model-Management
  Positive Constraints:
  - @mcp.tool() decorator verwendet
  - inference(prompt: str, model: str) -> str
  - Type-Hints für Auto-Schema
  - Docstrings als Tool-Description
  - Placeholder-Implementation
  GUTWILLIG:
  - MCP-konforme Tools
  INTELLIGENT:
  - FastMCP Auto-Schema
  KONTEXT-AWARE:
  - Parameter für LM Studio API
  FAUL:
  - Nur Tool-Definitionen
fallback: |
  Bei Komplexität: Minimal-Tool
```

```yaml
task: "2.8_implement_http_client"
directory: "units/lm-studio-bridge/logic/"
goal: |
  Implementiere async HTTP Client mit httpx für 
  LM Studio API Calls mit Connection Pool und Retry-Logic.
tools: |
  - Datei: units/lm-studio-bridge/logic/http_client.py
  - httpx AsyncClient
  - Environment-Config laden
work: |
  700 Token (HTTP-Client)
negative_constraints: |
  - KEINE synchronen Calls
  - KEINE unbegrenzten Retries
  - KEIN SDK-Code
validation: |
  Negative Constraints:
  - Kein LM Studio SDK
  - Keine Sync-Operations
  Positive Constraints:
  - AsyncClient mit Connection-Pool
  - base_url aus LM_STUDIO_URL env
  - Retry mit exponential backoff (max 3)
  - Timeout-Handling (30s default)
  - Methoden: get_models(), create_completion()
  GUTWILLIG:
  - Robuster HTTP-Client
  INTELLIGENT:
  - Connection-Reuse
  KONTEXT-AWARE:
  - host.docker.internal Support
  FAUL:
  - Nur HTTP-Calls
fallback: |
  Bei Komplexität: Basis-Client
```

```yaml
task: "2.9_implement_discovery_mechanism"
directory: "units/lm-studio-bridge/logic/"
goal: |
  Erstelle Discovery-Service mit 30-Sekunden Polling Loop
  für Model-Discovery über LM Studio /v1/models Endpoint.
tools: |
  - Datei: units/lm-studio-bridge/logic/discovery.py
  - asyncio für Polling-Loop
  - HTTP-Client aus logic/
work: |
  600 Token (Discovery-Service)
negative_constraints: |
  - KEINE Events außerhalb Unit
  - KEIN persistenter State
  - KEINE blockierenden Calls
validation: |
  Negative Constraints:
  - Kein Cross-Unit Code
  - Kein State-Storage
  Positive Constraints:
  - AsyncIO Task für Polling
  - 30 Sekunden Intervall (aus env)
  - GET /v1/models Call
  - In-Memory Model-Registry
  - Change-Detection (added/removed)
  GUTWILLIG:
  - Automatische Model-Erkennung
  INTELLIGENT:
  - Nur bei Änderungen updaten
  KONTEXT-AWARE:
  - LM Studio API-Format
  FAUL:
  - Nur Discovery-Loop
fallback: |
  Bei Error: Silent continue
```

```yaml
task: "2.10_implement_translation_layer"
directory: "units/lm-studio-bridge/logic/"
goal: |
  Implementiere Translation-Layer für OpenAI API Requests
  zu MCP Tool Calls mit Response-Mapping und Streaming.
tools: |
  - Datei: units/lm-studio-bridge/logic/translator.py
  - Pydantic für Daten-Models
  - httpx Response-Streaming
work: |
  800 Token (Translation-Logic)
negative_constraints: |
  - KEINE Custom-Protokolle
  - KEINE Modifikation von Responses
  - KEIN Caching
validation: |
  Negative Constraints:
  - Keine eigenen Formate
  - Kein Response-Caching
  Positive Constraints:
  - MCP Tool Call → OpenAI Completion Request
  - Parameter-Mapping (prompt, model, temperature)
  - Response-Streaming mit SSE
  - Error-Translation (HTTP → MCP Errors)
  - Vollständige Response-Weiterleitung
  GUTWILLIG:
  - Transparente Translation
  INTELLIGENT:
  - Streaming für Performance
  KONTEXT-AWARE:
  - OpenAI-kompatibles Format
  FAUL:
  - Nur Translation
fallback: |
  Bei Streaming-Issues: Fallback auf non-streaming
```

```yaml
task: "2.11_implement_lifecycle_handlers"
directory: "units/lm-studio-bridge/api/"
goal: |
  Implementiere MCP Lifecycle-Handler für Startup, Ready,
  Shutdown-Phasen mit Health-Check Integration.
tools: |
  - Datei: units/lm-studio-bridge/api/lifecycle.py
  - Platform Runtime imports
  - Integration in mcp_server.py
work: |
  500 Token (Lifecycle-Handler)
negative_constraints: |
  - KEINE langlebigen Connections
  - KEIN State zwischen Restarts
  - KEINE komplexen Shutdown-Prozesse
validation: |
  Negative Constraints:
  - Kein persistenter State
  - Keine langen Shutdowns
  Positive Constraints:
  - startup(): HTTP Client initialisieren
  - ready(): Erste Model-Liste geladen
  - shutdown(): Graceful Connection Close
  - health(): LM Studio erreichbar + Models > 0
  - Integration in MCP-Server
  GUTWILLIG:
  - Sauberer Lifecycle
  INTELLIGENT:
  - Schnelle Startup/Shutdown
  KONTEXT-AWARE:
  - MCP-Standard-Phasen
  FAUL:
  - Nur Required Handler
fallback: |
  Bei Fehler: Minimal-Implementation
```

```yaml
task: "2.12_create_bridge_dockerfile"
directory: "units/lm-studio-bridge/"
goal: |
  Erstelle optimierten Dockerfile mit python:3.11-alpine Base,
  Multi-Stage Build und Non-Root User für Security.
tools: |
  - Datei: units/lm-studio-bridge/Dockerfile
  - Multi-Stage Build Pattern
  - Alpine Linux Optimierungen
work: |
  600 Token (Dockerfile)
negative_constraints: |
  - KEINE Build-Tools im Final Image
  - KEINE Root-User Execution
  - KEINE unnötigen Packages
  - KEINE GPU-Dependencies
validation: |
  Negative Constraints:
  - Kein gcc/make im Final
  - Kein Root-User
  Positive Constraints:
  - FROM python:3.11-alpine AS builder
  - pip install --user für Dependencies
  - FROM python:3.11-alpine AS final
  - COPY --from=builder
  - USER 1000:1000
  - EXPOSE 3000
  GUTWILLIG:
  - Sicherer Container
  INTELLIGENT:
  - Multi-Stage für Size
  KONTEXT-AWARE:
  - Alpine für Container
  FAUL:
  - Minimal Image
fallback: |
  Bei Build-Fehler: Vereinfachen
```

```yaml
task: "2.13_create_start_script"
directory: "units/lm-studio-bridge/"
goal: |
  Erstelle start.sh Script das Platform Bootstrap lädt,
  Environment validiert und MCP Server startet.
tools: |
  - Datei: units/lm-studio-bridge/start.sh
  - Bash-Script
  - Python-Aufruf
work: |
  400 Token (Start-Script)
negative_constraints: |
  - KEINE komplexe Logik
  - KEINE Loops oder Waits
  - KEINE direkten Service-Starts
validation: |
  Negative Constraints:
  - Kein Service-Management
  - Keine komplexen Checks
  Positive Constraints:
  - #!/bin/sh (Alpine-kompatibel)
  - Export Python-Path für platform/
  - Validate Required Env-Vars
  - Start via uvicorn
  - Signal-Handling für Shutdown
  - Executable (chmod +x)
  GUTWILLIG:
  - Einfacher Start
  INTELLIGENT:
  - Platform-Integration
  KONTEXT-AWARE:
  - Alpine-Shell
  FAUL:
  - Nur Start-Logic
fallback: |
  Bei Shell-Fehler: Minimal-Version
```

```yaml
task: "2.14_create_mock_responses"
directory: "units/lm-studio-bridge/config/mocks/"
goal: |
  Erstelle Mock-JSON-Dateien für LM Studio API Responses
  zum Testen ohne laufenden LM Studio Server.
tools: |
  - models_response.json
  - completion_response.json
  - error_response.json
  - JSON-Format
work: |
  400 Token (Mock-Daten)
negative_constraints: |
  - KEINE echten Model-Daten
  - KEINE großen Responses
  - KEINE sensitive Infos
validation: |
  Negative Constraints:
  - Keine Real-Data
  - Keine API-Keys
  Positive Constraints:
  - models_response.json mit 2 Beispiel-Models
  - completion_response.json mit Stream-Chunks
  - error_response.json mit Standard-Errors
  - OpenAI-kompatibles Format
  GUTWILLIG:
  - Testbare Unit
  INTELLIGENT:
  - Realistische Mocks
  KONTEXT-AWARE:
  - LM Studio Response-Format
  FAUL:
  - Nur Test-Daten
fallback: |
  Bei Format-Unsicherheit: OpenAI Docs
```

```yaml
task: "2.15_test_container_build"
directory: "units/lm-studio-bridge/"
goal: |
  Erstelle test-build.sh Script zum Testen des Container-Builds
  und basis Health-Check ohne externe Dependencies.
tools: |
  - Datei: units/lm-studio-bridge/test-build.sh
  - Docker Build Command
  - Basis-Smoke-Test
work: |
  300 Token (Test-Script)
negative_constraints: |
  - KEINE Integration-Tests
  - KEINE externen Services
  - KEIN Push zu Registry
validation: |
  Negative Constraints:
  - Kein LM Studio Required
  - Kein Network-Test
  Positive Constraints:
  - docker build -t lm-bridge:test .
  - docker run --rm lm-bridge:test --version
  - Exit-Code Check
  - Build-Time < 2 Minuten
  - Clean-Up nach Test
  GUTWILLIG:
  - Schneller Build-Test
  INTELLIGENT:
  - Nur Smoke-Test
  KONTEXT-AWARE:
  - Docker Desktop
  FAUL:
  - Minimal Test
fallback: |
  Bei Docker-Fehler: Skip Test
```

