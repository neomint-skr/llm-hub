# LLM Hub Control Center

Single control point where users can see status and fix ANY issue with one click.

## Overview

The Control Center provides a unified interface for managing LLM Hub with zero technical complexity:

- **Real-time Status** - See all service health at a glance
- **One-Click Fixes** - Resolve common issues instantly
- **System Tray Integration** - Quick access from Windows system tray
- **No Technical Jargon** - Simple, user-friendly interface

## Features

### 🎯 One-Click Problem Resolution

Every common issue has a dedicated fix button:

- **Fix Docker Issues** - Restart containers, clean up resources
- **Fix LM Studio Connection** - Reconnect bridge, restart services
- **Fix Port Conflicts** - Detect and resolve port usage conflicts
- **Reset Configuration** - Restore default settings

### 📊 Real-Time Monitoring

- Gateway service status
- Bridge service status  
- LM Studio connectivity
- Docker container health
- System resource usage

### 🖥️ Multiple Access Methods

1. **Web Interface** - Full-featured control panel
2. **System Tray** - Quick actions from Windows tray
3. **API Endpoints** - Programmatic access

## Quick Start

### Start Control Center

```cmd
start-control-center.bat
```

This will:
- Start the Control API server on port 9000
- Optionally start system tray integration
- Open the web interface automatically

### Access Methods

- **Web Interface**: http://localhost:9000
- **System Tray**: Right-click the LLM Hub icon in system tray
- **API Documentation**: http://localhost:9000/docs

## Web Interface

### Main Dashboard

The web interface provides:

- **System Status Card** - Overall health overview
- **Service Control Card** - Start/stop/restart services
- **Quick Fixes Card** - One-click problem resolution
- **Quick Actions** - Common tasks and utilities

### One-Click Actions

| Action | Description |
|--------|-------------|
| Start All Services | Launch all LLM Hub services |
| Restart All Services | Restart services to resolve issues |
| Stop All Services | Gracefully stop all services |
| Fix Docker Issues | Clean containers, restart services |
| Fix LM Studio Connection | Reconnect bridge to LM Studio |
| Fix Port Conflicts | Resolve port usage conflicts |
| Reset Configuration | Restore default settings |
| Run Diagnostics | Check system health |
| Setup Autostart | Configure automatic startup |

## System Tray Integration

### Features

- **Status Indicator** - Icon color shows system health
- **Quick Actions Menu** - Right-click for common tasks
- **Background Monitoring** - Continuous health checking
- **System Notifications** - Alerts for status changes

### Tray Menu

- LLM Hub Control Center (opens web interface)
- Status (show current health)
- Start/Restart/Stop Services
- Quick Fixes submenu
- Open Dashboard
- View Logs
- Run Diagnostics
- Setup Autostart
- Documentation
- Exit

## API Reference

### Control Commands

All commands are POST requests to `/api/commands/{command}`:

```bash
# Start all services
curl -X POST http://localhost:9000/api/commands/start-services

# Fix Docker issues
curl -X POST http://localhost:9000/api/commands/fix-docker

# Run diagnostics
curl -X POST http://localhost:9000/api/commands/run-diagnostics
```

### Available Commands

- `start-services` - Start all LLM Hub services
- `restart-services` - Restart all services
- `stop-services` - Stop all services
- `fix-docker` - Fix Docker-related issues
- `fix-lmstudio` - Fix LM Studio connection
- `fix-ports` - Fix port conflicts
- `reset-config` - Reset configuration
- `run-diagnostics` - Run system diagnostics
- `setup-autostart` - Configure autostart

### Status Endpoint

```bash
# Get system status
curl http://localhost:9000/api/status
```

Returns comprehensive status for all components.

## Architecture

### Components

1. **Control API** (`control_api.py`) - FastAPI backend
2. **Web Interface** (`index.html`, `control.js`) - Frontend
3. **System Tray** (`system_tray.py`) - Windows integration

### Design Principles

- **Zero Complexity** - No technical knowledge required
- **One-Click Solutions** - Every problem has a button
- **Windows Native** - Follows Windows UI patterns
- **Fail-Safe** - Conservative actions, clear feedback

## Troubleshooting

### Control Center Won't Start

1. Check Python installation: `python --version`
2. Install missing packages: `pip install fastapi uvicorn`
3. Check port 9000 availability
4. Run manually: `python ops/control/control_api.py`

### System Tray Not Working

1. Install required packages: `pip install pystray pillow`
2. Check Windows permissions
3. Run manually: `python ops/control/system_tray.py`

### Commands Fail

1. Check if LLM Hub services are accessible
2. Verify Docker Desktop is running
3. Check network connectivity
4. Review API logs for details

## Security

- **Local Only** - Control API binds to localhost
- **No Authentication** - Designed for single-user systems
- **Safe Commands** - No destructive operations
- **User Confirmation** - Prompts for dangerous actions

## Customization

### Adding New Commands

1. Add command handler to `control_api.py`
2. Add button to `index.html`
3. Add JavaScript function to `control.js`
4. Add menu item to `system_tray.py`

### Styling Changes

Modify CSS variables in `index.html`:

```css
:root {
    --primary-color: #2196F3;
    --success-color: #4CAF50;
    --warning-color: #FF9800;
    --danger-color: #f44336;
}
```

## Dependencies

### Required
- Python 3.8+
- fastapi
- uvicorn

### Optional (System Tray)
- pystray
- pillow
- win10toast (Windows notifications)
