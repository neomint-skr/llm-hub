# "Show Me!" Test Framework

User-friendly testing that demonstrates working functionality with clear visual feedback.

## Overview

The "Show Me!" Test Framework provides an intuitive way to verify that LLM Hub is working correctly. Instead of technical test output, it shows clear visual feedback that any user can understand.

## Features

### 🎯 User-Friendly Testing

- **Visual Feedback** - Clear ✅/❌ indicators for each test
- **Plain English** - No technical jargon, just clear explanations
- **Real-Time Progress** - See tests running in real-time
- **Detailed Results** - Get specific information about what's working

### 🔍 Comprehensive Coverage

Tests all major components:

- **Infrastructure** - Docker services, health checks
- **Integration** - LM Studio connection, MCP tools
- **Advanced Features** - Autostart, Control Center, Predictive Maintenance
- **End-to-End** - Complete workflow validation

### 📊 Clear Reporting

- **Test Summary** - Pass/fail counts and success rate
- **Failure Details** - Specific error messages and solutions
- **Performance Metrics** - Response times and data points
- **Overall Status** - Clear final result

## Quick Start

### Run Tests

```cmd
show-me.bat
```

This will:
1. Check Python and install required packages
2. Run all "Show Me!" tests
3. Display results with clear visual feedback
4. Provide next steps based on results

### Manual Execution

```cmd
cd ops\testing
python show_me_framework.py
```

## Test Categories

### Core Infrastructure Tests

| Test | Description | Success Criteria |
|------|-------------|------------------|
| Docker Services Running | Verifies Docker containers are active | 2+ LLM Hub services running |
| Gateway Health Check | Tests gateway responsiveness | HTTP 200 from /health endpoint |
| Bridge Health Check | Tests bridge connectivity | HTTP 200 from bridge /health |

### Integration Tests

| Test | Description | Success Criteria |
|------|-------------|------------------|
| LM Studio Connection | Verifies LM Studio accessibility | HTTP 200 from /v1/models endpoint |
| MCP Tools Discovery | Tests tool enumeration | 1+ MCP tools discovered |
| End-to-End Inference | Validates complete workflow | Inference tools available |

### Advanced Features Tests

| Test | Description | Success Criteria |
|------|-------------|------------------|
| Autostart Configuration | Checks Windows Task Scheduler | Task "LLM Hub Autostart" exists |
| Control Center Available | Tests control interface | HTTP 200 from port 9000 |
| Predictive Maintenance Active | Verifies monitoring system | Monitoring active with data points |

## Understanding Results

### Test Status Icons

- ✅ **PASSED** - Test completed successfully
- ❌ **FAILED** - Test failed, check error message
- 🔄 **RUNNING** - Test currently executing
- ⏭️ **SKIPPED** - Test was skipped due to dependencies

### Common Failure Scenarios

#### Docker Services Not Running
```
❌ Docker Services Running (0.15s)
   💬 Found 0 LLM Hub services running
```
**Solution**: Run `start.bat` to start LLM Hub services

#### LM Studio Not Connected
```
❌ LM Studio Connection (5.02s)
   💬 LM Studio not running or not accessible
```
**Solution**: Start LM Studio and enable Local Server on port 1234

#### Control Center Not Available
```
❌ Control Center Available (5.01s)
   💬 Control Center not running - start with start-control-center.bat
```
**Solution**: Run `start-control-center.bat` to start the control interface

### Success Example

```
🚀 LLM Hub 'Show Me!' Test Framework
==================================================
Demonstrating working functionality with visual feedback

🔄 Docker Services Running...
✅ Docker Services Running (0.23s)
   💬 Found 2 LLM Hub services running
   📊 services_count: 2

🔄 Gateway Health Check...
✅ Gateway Health Check (0.15s)
   💬 Gateway healthy - Status: healthy
   📊 response_time: 0.142

🔄 Bridge Health Check...
✅ Bridge Health Check (0.12s)
   💬 Bridge healthy - Service: lm-studio-bridge
   📊 response_time: 0.118

📊 Test Summary
==================================================
Total Tests: 9
✅ Passed: 9
❌ Failed: 0
⏱️  Total Duration: 2.45s
📈 Success Rate: 100.0%

🎯 Overall Status: ✅ ALL TESTS PASSED
==================================================
```

## Integration with Existing Tests

The "Show Me!" framework complements existing technical tests:

- **Technical Tests** (`ops/scripts/`) - For developers and CI/CD
- **"Show Me!" Tests** (`ops/testing/`) - For users and validation

Both test suites can be run independently or together.

## Customization

### Adding New Tests

1. Add test method to `ShowMeTestFramework` class:
```python
def test_my_feature(self) -> tuple:
    """Test: My feature works"""
    try:
        # Test logic here
        return True, "Feature is working", {"detail": "value"}
    except Exception as e:
        return False, f"Feature failed: {e}", None
```

2. Add to test execution in `run_all_tests()`:
```python
await self.run_test("My Feature Test", self.test_my_feature)
```

### Modifying Test Criteria

Edit the test methods to change success criteria:

```python
def test_gateway_health(self) -> tuple:
    # Modify timeout, endpoints, or success criteria
    response = requests.get(f"{self.gateway_url}/health", timeout=5)  # Changed from 10
    # ... rest of test logic
```

## Troubleshooting

### Python Not Found
```
❌ ERROR: Python is not installed or not in PATH
```
Install Python 3.8+ from https://python.org

### Package Installation Fails
```
❌ ERROR: Failed to install required packages
```
Run as administrator or check internet connection

### All Tests Fail
```
❌ Cannot connect to Gateway
❌ Cannot connect to Bridge
```
1. Check if Docker Desktop is running
2. Run `start.bat` to start services
3. Wait for services to fully initialize

### Partial Failures
Some tests pass, others fail - check specific error messages for targeted solutions.

## Architecture

### Framework Components

- **ShowMeTestFramework** - Main test orchestrator
- **TestResult** - Individual test result container
- **TestStatus** - Test execution state enumeration

### Design Principles

- **User-Centric** - Designed for end users, not developers
- **Visual Clarity** - Clear icons and progress indicators
- **Actionable Feedback** - Specific solutions for failures
- **Non-Technical Language** - Avoids technical jargon

### Dependencies

- **requests** - HTTP client for endpoint testing
- **subprocess** - System command execution
- **asyncio** - Asynchronous test execution
- **json** - Response data parsing
