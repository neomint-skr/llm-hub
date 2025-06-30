# LLM Hub Autostart System

Complete autostart chain that eliminates all manual startup steps.

## Overview

The autostart system creates a fully automated startup sequence:

1. **Windows Startup** → Task Scheduler (30s delay)
2. **Task Scheduler** → Docker Desktop startup wait (up to 5 minutes)
3. **Docker Desktop** → LM Studio auto-launch detection
4. **LM Studio** → LLM Hub services startup
5. **Services** → Health check verification

## Installation

Run from the LLM Hub root directory:

```cmd
setup-autostart.bat
```

This will:
- Register a Windows Task Scheduler task
- Configure automatic startup on user login
- Set appropriate delays for dependency startup

## Features

### Zero User Interaction
- No prompts or manual steps required
- Automatic dependency detection and waiting
- Smart retry logic for all components

### Intelligent Startup Sequence
- Waits for Docker Desktop (up to 5 minutes)
- Auto-detects and launches LM Studio if needed
- Verifies service health before completion

### Windows Integration
- Uses native Windows Task Scheduler
- No administrator privileges required
- Respects Windows startup timing

## Configuration

### Task Scheduler Settings
- **Trigger**: User logon + 30 second delay
- **Conditions**: Network available, not on battery
- **Settings**: Allow start on demand, restart on failure

### Startup Timeouts
- Docker Desktop: 5 minutes maximum wait
- LM Studio: 2 minutes maximum wait
- Service health: 1 minute maximum wait

## Management

### Check Status
```cmd
schtasks /query /tn "LLM Hub Autostart"
```

### Test Autostart
```cmd
schtasks /run /tn "LLM Hub Autostart"
```

### Remove Autostart
```cmd
remove-autostart.bat
```

## Troubleshooting

### Common Issues

**Docker Desktop not starting**
- Ensure Docker Desktop is properly installed
- Check Windows startup programs for Docker
- Verify Docker Desktop auto-start is enabled

**LM Studio not found**
- Install LM Studio in standard location
- Verify LM Studio is configured for port 1234
- Check LM Studio auto-server settings

**Services not starting**
- Check Docker Desktop is fully initialized
- Verify port 8080 is available
- Review logs with `logs.bat`

### Log Files

Autostart logs are written to Windows Event Log under:
- Application and Services Logs
- Task Scheduler
- LLM Hub Autostart

## Architecture

### Dependency Chain
```
Windows Login
    ↓ (30s delay)
Task Scheduler
    ↓ (wait up to 5min)
Docker Desktop
    ↓ (detect/launch)
LM Studio
    ↓ (health check)
LLM Hub Services
```

### Failure Handling
- Each step has timeout and retry logic
- Non-critical failures are logged but don't stop the chain
- Critical failures exit with clear error messages

## Security

- Runs with user privileges (no elevation required)
- Uses Windows native scheduling (no third-party tools)
- Respects Windows security policies
- No network access during setup
