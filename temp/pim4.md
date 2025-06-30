```yaml
task: "7.1_implement_full_autostart_chain"
directory: "/"
goal: |
  Create complete autostart chain: Windows → Docker → LM Studio → Services
  so user never needs to start anything manually.
tools: |
  - Windows Task Scheduler integration
  - start.bat enhancement
  - LM Studio auto-launch
  - Wait and retry logic
work: |
  800 Token (Full autostart)
negative_constraints: |
  - NO user prompts
  - NO manual steps
  - NO admin elevation
validation: |
  GUTWILLIG:
  - User macht NIE wieder was manuell
  INTELLIGENT:
  - Nutzt Windows-native Features
  - Smart wait for dependencies
  KONTEXT-AWARE:
  - Docker Desktop startup time
  - LM Studio load time
  FAUL:
  - Kein Code der nicht zur Intention beiträgt
fallback: |
  If component missing: Auto-download or clear message
```

```yaml
task: "7.2_implement_complete_error_recovery"
directory: "units/lm-studio-bridge/"
goal: |
  Make bridge recover from ALL common errors automatically
  without user intervention ever needed.
tools: |
  - Enhanced error handlers
  - Automatic reconnection
  - Service restart logic
  - State recovery
work: |
  1000 Token (Complete recovery)
negative_constraints: |
  - NO error reaches user
  - NO manual restart needed
  - NO data loss
validation: |
  GUTWILLIG:
  - JEDER Fehler wird automatisch behoben
  INTELLIGENT:
  - Circuit breaker für pathologische Fälle
  - Exponential backoff
  KONTEXT-AWARE:
  - Windows/Docker specific errors
  - Network transience
  FAUL:
  - Nur Error-Handler, kein neuer Service
fallback: |
  If unrecoverable: Clear user action (one button)
```

```yaml
task: "7.3_implement_intelligent_resource_management"
directory: "units/lm-studio-bridge/"
goal: |
  Implement automatic resource adjustment so system NEVER
  impacts user's other activities or crashes.
tools: |
  - CPU/Memory monitoring
  - Dynamic limit adjustment
  - Predictive throttling
work: |
  600 Token (Resource management)
negative_constraints: |
  - NO performance degradation for user
  - NO manual limit setting
  - NO crashes ever
validation: |
  GUTWILLIG:
  - User's PC bleibt IMMER responsive
  INTELLIGENT:
  - Nutzt Docker's native limits
  - Simple 50% rule implementation
  KONTEXT-AWARE:
  - Windows activity detection
  FAUL:
  - In bestehende Services integriert
fallback: |
  If detection fails: Conservative defaults
```

```yaml
task: "7.4_create_unified_control_interface"
directory: "ops/control/"
goal: |
  Create single control point where user can see status
  and fix ANY issue with one click.
tools: |
  - Minimal web UI
  - System tray integration
  - One-click fixes
work: |
  800 Token (Control interface)
negative_constraints: |
  - NO complex UI
  - NO technical jargon
  - NO multi-step processes
validation: |
  GUTWILLIG:
  - JEDES Problem mit einem Klick lösbar
  INTELLIGENT:
  - Zeigt nur was wichtig ist
  - Auto-fix Buttons für alles
  KONTEXT-AWARE:
  - Windows UI patterns
  FAUL:
  - Minimales UI, maximaler Effekt
fallback: |
  If UI fails: Tray icon with restart option
```

```yaml
task: "7.5_implement_predictive_maintenance"
directory: "units/health-monitor/"
goal: |
  Detect and fix problems BEFORE user notices them
  through predictive patterns and preemptive action.
tools: |
  - Trend analysis
  - Preemptive cleanup
  - Resource prediction
  - Proactive healing
work: |
  600 Token (Predictive system)
negative_constraints: |
  - NO false positives
  - NO unnecessary actions
  - NO user notifications
validation: |
  GUTWILLIG:
  - Probleme werden verhindert, nicht behoben
  INTELLIGENT:
  - Simple patterns (memory growth = cleanup)
  KONTEXT-AWARE:
  - Common Windows issues
  FAUL:
  - Nutzt bestehende Metriken
fallback: |
  If prediction wrong: Normal healing kicks in
```

# Tasks für "Show Me!" Test-Integration in LLM Hub

## Phase 8: Show Me Test Framework

```yaml
task: "8.1_create_test_orchestrator"
directory: "ops/testing/"
goal: |
  Create test orchestrator that automates the "Show Me!" methodology
  with automatic evidence collection and report generation.
tools: |
  - New directory: ops/testing/
  - Python script: show_me_test.py
  - Screenshot capability (Pillow)
  - Terminal capture
work: |
  800 Token (Test orchestrator)
negative_constraints: |
  - NO complex test frameworks
  - NO external test services
  - NO manual evidence collection
  - NO simulated tests
validation: |
  GUTWILLIG:
  - Makes testing foolproof for agents
  - Automatic evidence collection
  INTELLIGENT:
  - Uses Windows screenshot API
  - Captures terminal automatically
  KONTEXT-AWARE:
  - Windows-specific tools
  - Docker Desktop integration
  FAUL:
  - Only code that ensures real testing
fallback: |
  If screenshot fails: Use terminal-only evidence
```

```yaml
task: "8.2_implement_cold_start_test"
directory: "ops/testing/"
goal: |
  Implement automated cold start test that verifies system
  starts correctly with full evidence capture.
tools: |
  - Script: tests/cold_start_test.py
  - Process monitoring
  - Port checking
  - Log capture
work: |
  600 Token (Cold start test)
negative_constraints: |
  - NO mocking of services
  - NO skipping error checks
  - NO timeout shortcuts
  - NO success simulation
validation: |
  GUTWILLIG:
  - Catches all startup failures
  - Clear evidence of success
  INTELLIGENT:
  - Monitors actual processes
  - Real health checks
  KONTEXT-AWARE:
  - Docker Desktop startup time
  - Windows process names
  FAUL:
  - Reuses existing health endpoints
fallback: |
  If service won't start: Full error dump
```

```yaml
task: "8.3_implement_performance_test"
directory: "ops/testing/"
goal: |
  Create automated performance test that measures and documents
  LM Studio response times with evidence.
tools: |
  - Script: tests/performance_test.py
  - httpx for timing
  - Concurrent request testing
  - Statistics generation
work: |
  700 Token (Performance test)
negative_constraints: |
  - NO fake metrics
  - NO averaged-out outliers
  - NO performance estimates
  - NO cached responses
validation: |
  GUTWILLIG:
  - Shows real performance to user
  - Fails if too slow
  INTELLIGENT:
  - Measures TTFB, streaming
  - GPU utilization check
  KONTEXT-AWARE:
  - LM Studio token rates
  - Windows performance counters
  FAUL:
  - Only metrics that matter
fallback: |
  If performance bad: Clear report why
```

```yaml
task: "8.4_implement_gui_interaction_test"
directory: "ops/testing/"
goal: |
  Automate GUI testing for Control Center with screenshot
  evidence of every interaction and state.
tools: |
  - Script: tests/gui_test.py
  - Selenium WebDriver
  - Screenshot at each step
  - State verification
work: |
  600 Token (GUI test)
negative_constraints: |
  - NO headless mode
  - NO skipped interactions
  - NO assumed states
  - NO timing races
validation: |
  GUTWILLIG:
  - Proves GUI actually works
  - Every button tested
  INTELLIGENT:
  - Real browser automation
  - Visual regression detection
  KONTEXT-AWARE:
  - Windows screenshot API
  - Browser compatibility
  FAUL:
  - Only user-visible features
fallback: |
  If GUI fails: Screenshot of error
```

```yaml
task: "8.5_implement_error_recovery_test"
directory: "ops/testing/"
goal: |
  Test and document system recovery from common failures
  with evidence of self-healing behavior.
tools: |
  - Script: tests/recovery_test.py
  - Service manipulation
  - Process killing
  - Recovery monitoring
work: |
  700 Token (Recovery test)
negative_constraints: |
  - NO gentle failures
  - NO pre-warned system
  - NO recovery assistance
  - NO partial tests
validation: |
  GUTWILLIG:
  - Proves self-healing works
  - Documents recovery time
  INTELLIGENT:
  - Real failure injection
  - Measures recovery metrics
  KONTEXT-AWARE:
  - Windows process management
  - Docker container handling
  FAUL:
  - Tests only promised features
fallback: |
  If no recovery: Document failure mode
```

```yaml
task: "8.6_create_evidence_collector"
directory: "ops/testing/"
goal: |
  Build automatic evidence collection system that captures
  screenshots, logs, metrics during all tests.
tools: |
  - Module: evidence_collector.py
  - Screenshot library
  - Log aggregation
  - Metric capture
work: |
  600 Token (Evidence system)
negative_constraints: |
  - NO manual screenshots
  - NO log editing
  - NO cherry-picking
  - NO evidence loss
validation: |
  GUTWILLIG:
  - Makes lying impossible
  - Full transparency
  INTELLIGENT:
  - Automatic timestamping
  - Organized file structure
  KONTEXT-AWARE:
  - Windows paths
  - Multiple monitor support
  FAUL:
  - Only captures what's needed
fallback: |
  If capture fails: Note in report
```

```yaml
task: "8.7_create_report_generator"
directory: "ops/testing/"
goal: |
  Generate beautiful HTML/Markdown reports from test runs
  with all evidence embedded and linked.
tools: |
  - Module: report_generator.py
  - HTML/CSS templates
  - Markdown export
  - Evidence embedding
work: |
  600 Token (Report generator)
negative_constraints: |
  - NO hiding failures
  - NO summary without evidence
  - NO success without proof
  - NO manual editing
validation: |
  GUTWILLIG:
  - Clear pass/fail for user
  - All evidence accessible
  INTELLIGENT:
  - Responsive HTML design
  - Filterable results
  KONTEXT-AWARE:
  - Opens in default browser
  - Windows path handling
  FAUL:
  - Reuses test outputs
fallback: |
  If HTML fails: Plain text report
```

```yaml
task: "8.8_create_continuous_test_mode"
directory: "ops/testing/"
goal: |
  Implement continuous testing mode that runs "Show Me!"
  tests periodically to ensure system stays healthy.
tools: |
  - Script: continuous_test.py
  - Scheduled test runs
  - Notification system
  - Historical tracking
work: |
  500 Token (Continuous mode)
negative_constraints: |
  - NO invasive testing
  - NO performance impact
  - NO false positives
  - NO notification spam
validation: |
  GUTWILLIG:
  - Catches degradation early
  - User stays informed
  INTELLIGENT:
  - Adaptive test frequency
  - Smart notifications
  KONTEXT-AWARE:
  - Windows Task Scheduler
  - System tray integration
  FAUL:
  - Minimal background impact
fallback: |
  If scheduling fails: Manual run option
```

```yaml
task: "8.9_integrate_with_cicd"
directory: "ops/testing/"
goal: |
  Create CI/CD integration that requires "Show Me!" tests
  to pass before any deployment or release.
tools: |
  - GitHub Actions workflow
  - Test runner script
  - Evidence artifact upload
  - Badge generation
work: |
  400 Token (CI/CD integration)
negative_constraints: |
  - NO test skipping
  - NO manual overrides
  - NO cached results
  - NO partial runs
validation: |
  GUTWILLIG:
  - Ensures quality releases
  - Public evidence
  INTELLIGENT:
  - Artifact preservation
  - Badge automation
  KONTEXT-AWARE:
  - GitHub Actions specific
  - Windows runner support
  FAUL:
  - Reuses existing tests
fallback: |
  If CI fails: Local test mandatory
```

```yaml
task: "8.10_create_test_documentation"
directory: "docs/testing/"
goal: |
  Document the complete "Show Me!" test suite with examples
  and instructions for running and interpreting tests.
tools: |
  - Create: docs/testing/README.md
  - Test case documentation
  - Evidence examples
  - Troubleshooting guide
work: |
  500 Token (Documentation)
negative_constraints: |
  - NO complex procedures
  - NO assumed knowledge
  - NO missing steps
  - NO technical jargon
validation: |
  GUTWILLIG:
  - Anyone can run tests
  - Clear success criteria
  INTELLIGENT:
  - Visual examples
  - Common issues covered
  KONTEXT-AWARE:
  - Windows-specific steps
  - Docker Desktop issues
  FAUL:
  - Focus on running, not theory
fallback: |
  If unclear: Add more examples
```

```yaml
task: "9.1_implement_rule0_linter"
directory: "ops/ci/"
goal: |
  Implement comprehensive Rule-0 linter that enforces all
  dedardf structural rules with clear violation reporting.
tools: |
  - Create: ops/ci/rule0-check.sh
  - Shell script with find/grep
  - Comprehensive path checking
  - CI integration ready
work: |
  500 Token (Rule-0 linter)
negative_constraints: |
  - NO false positives
  - NO missed violations
  - NO complex regex
  - NO external dependencies
validation: |
  GUTWILLIG:
  - Helps maintain clean structure
  - Clear error messages
  INTELLIGENT:
  - Fast execution
  - Precise pattern matching
  KONTEXT-AWARE:
  - Git-aware (ignores .git)
  - Docker-aware (ignores images)
  FAUL:
  - Only checks what matters
fallback: |
  If pattern unclear: Err on strict side
```

```yaml
task: "9.2_create_unit_manifests"
directory: "units/"
goal: |
  Create unit-manifest.json for each unit with complete
  metadata for service discovery and automation.
tools: |
  - Create: units/*/unit-manifest.json
  - JSON schema compliance
  - MCP metadata included
  - Discovery configuration
work: |
  600 Token (Unit manifests)
negative_constraints: |
  - NO manual maintenance
  - NO version conflicts
  - NO missing fields
  - NO invalid JSON
validation: |
  GUTWILLIG:
  - Enables automatic discovery
  - Self-documenting units
  INTELLIGENT:
  - Validates against schema
  - Version from unit.yml
  KONTEXT-AWARE:
  - MCP-specific fields
  - Docker service names
  FAUL:
  - Generated from existing data
fallback: |
  If generation fails: Template provided
```

```yaml
task: "9.3_implement_mcp_orchestrator"
directory: "platform/runtime/"
goal: |
  Create MCP lifecycle orchestrator that coordinates all
  MCP services using standardized lifecycle commands.
tools: |
  - Create: platform/runtime/mcp_orchestrator.py
  - Async lifecycle management
  - Service state tracking
  - Event coordination
work: |
  800 Token (MCP orchestrator)
negative_constraints: |
  - NO service-specific logic
  - NO hardcoded endpoints
  - NO blocking operations
  - NO state persistence
validation: |
  GUTWILLIG:
  - Graceful service coordination
  - Clean shutdown sequences
  INTELLIGENT:
  - Parallel lifecycle ops
  - Dependency ordering
  KONTEXT-AWARE:
  - MCP standard phases
  - Container lifecycle
  FAUL:
  - Reuses health checks
fallback: |
  If orchestration fails: Independent mode
```

```yaml
task: "9.4_add_contract_diff_checking"
directory: "ops/ci/"
goal: |
  Implement contract breaking change detection using
  OpenAPI diff tools in CI pipeline.
tools: |
  - Script: ops/ci/contract-check.sh
  - OpenAPI diff tool
  - Git integration
  - CI workflow update
work: |
  500 Token (Contract checking)
negative_constraints: |
  - NO manual diff review
  - NO ignored changes
  - NO version downgrades
  - NO silent breaks
validation: |
  GUTWILLIG:
  - Prevents breaking changes
  - Clear change documentation
  INTELLIGENT:
  - Semantic versioning
  - Automated checks
  KONTEXT-AWARE:
  - Git history aware
  - PR integration
  FAUL:
  - Only on contract changes
fallback: |
  If diff fails: Block merge
```

```yaml
task: "9.5_create_discovery_registry"
directory: "platform/runtime/"
goal: |
  Build automatic service discovery registry that uses
  unit manifests for dynamic service registration.
tools: |
  - Module: discovery_registry.py
  - Manifest parsing
  - Health integration
  - API exposure
work: |
  600 Token (Discovery registry)
negative_constraints: |
  - NO manual registration
  - NO static configs
  - NO memory leaks
  - NO stale entries
validation: |
  GUTWILLIG:
  - Zero-config discovery
  - Always accurate
  INTELLIGENT:
  - Health-based availability
  - Automatic cleanup
  KONTEXT-AWARE:
  - Docker service names
  - Container networking
  FAUL:
  - Reuses manifests
fallback: |
  If discovery fails: Static fallback
```

```yaml
task: "9.6_implement_structure_validator"
directory: "ops/ci/"
goal: |
  Create comprehensive structure validator ensuring
  all units follow dedardf patterns exactly.
tools: |
  - Script: structure-validate.py
  - Directory structure checks
  - File presence validation
  - Import analysis
work: |
  600 Token (Structure validator)
negative_constraints: |
  - NO exceptions allowed
  - NO partial compliance
  - NO legacy patterns
  - NO workarounds
validation: |
  GUTWILLIG:
  - Maintains consistency
  - Prevents drift
  INTELLIGENT:
  - Clear violation reports
  - Suggested fixes
  KONTEXT-AWARE:
  - dedardf rules
  - MCP requirements
  FAUL:
  - Reuses Rule-0 patterns
fallback: |
  If structure bad: Detailed report
```

```yaml
task: "9.7_add_pre_commit_hooks"
directory: ".config/"
goal: |
  Install pre-commit hooks that run all dedardf validators
  before allowing commits to repository.
tools: |
  - Create: .config/pre-commit.yaml
  - Git hooks setup
  - Validator integration
  - Developer guide
work: |
  400 Token (Pre-commit setup)
negative_constraints: |
  - NO commit if failing
  - NO bypass without flag
  - NO slow checks
  - NO false positives
validation: |
  GUTWILLIG:
  - Catches issues early
  - Saves review time
  INTELLIGENT:
  - Only changed files
  - Fast execution
  KONTEXT-AWARE:
  - Git workflow
  - Developer experience
  FAUL:
  - Reuses validators
fallback: |
  If hooks fail: Manual check required
```

```yaml
task: "9.8_create_unit_generator"
directory: "ops/tools/"
goal: |
  Build unit generator tool that creates compliant unit
  structure with all required files and configurations.
tools: |
  - Script: generate-unit.py
  - Template system
  - Interactive prompts
  - Validation built-in
work: |
  700 Token (Unit generator)
negative_constraints: |
  - NO non-compliant output
  - NO manual steps after
  - NO missing files
  - NO wrong patterns
validation: |
  GUTWILLIG:
  - Makes compliance easy
  - Reduces errors
  INTELLIGENT:
  - Smart defaults
  - MCP detection
  KONTEXT-AWARE:
  - Project conventions
  - Existing patterns
  FAUL:
  - Templates, not code
fallback: |
  If generation fails: Manual template
```

```yaml
task: "9.9_implement_audit_system"
directory: "ops/audit/"
goal: |
  Create continuous audit system that monitors dedardf
  compliance and generates compliance reports.
tools: |
  - Module: audit_system.py
  - Scheduled checks
  - Report generation
  - Trend analysis
work: |
  600 Token (Audit system)
negative_constraints: |
  - NO performance impact
  - NO false alerts
  - NO manual reports
  - NO data loss
validation: |
  GUTWILLIG:
  - Maintains quality
  - Early warning system
  INTELLIGENT:
  - Trend detection
  - Root cause analysis
  KONTEXT-AWARE:
  - Git history
  - Change patterns
  FAUL:
  - Reuses all validators
fallback: |
  If audit fails: Manual check mode
```

```yaml
task: "9.10_document_dedardf_compliance"
directory: "docs/architecture/"
goal: |
  Create comprehensive dedardf compliance guide with
  examples, anti-patterns, and automation tools.
tools: |
  - Create: docs/architecture/dedardf-guide.md
  - Visual diagrams
  - Tool documentation
  - Checklist format
work: |
  500 Token (Compliance guide)
negative_constraints: |
  - NO ambiguity
  - NO contradictions
  - NO outdated info
  - NO missing tools
validation: |
  GUTWILLIG:
  - Makes compliance clear
  - Prevents violations
  INTELLIGENT:
  - Examples for each rule
  - Common mistakes covered
  KONTEXT-AWARE:
  - LLM Hub specific
  - Tool integration
  FAUL:
  - References, not duplicates
fallback: |
  If unclear: Add more examples
```
