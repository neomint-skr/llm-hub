# LLM Hub - Zero-Configuration MCP Bridge

A minimal platform for bridging LM Studio with MCP-compatible clients through a unified gateway architecture.

## Overview

LLM Hub provides seamless integration between LM Studio and MCP (Model Context Protocol) compatible applications. The platform automatically discovers available models and exposes them as standardized MCP tools through a unified API gateway.

## Features

- **Zero-Configuration Setup** - Works out of the box with LM Studio
- **Automatic Model Discovery** - Dynamically detects and exposes available models
- **MCP 2025-06-18 Compliance** - Full compatibility with latest MCP specification
- **Unified Gateway** - Single endpoint for all model interactions
- **Docker-Based Deployment** - Containerized services for easy management
- **Windows-Optimized** - Designed specifically for Windows development environments
- **Authentication & Rate Limiting** - Built-in security and usage controls
- **Health Monitoring** - Comprehensive service health checks and monitoring

## Quick Start

### Prerequisites

- Windows 10/11
- Docker Desktop
- LM Studio (running with local server enabled)

### Manual Installation

1. **Start LM Studio** - Launch application, load model, enable Local Server (port 1234)
2. **Launch LLM Hub** - Run start.bat
3. **Verify Installation** - Check http://localhost:8080/health

### Automatic Installation (Recommended)

1. **Setup Autostart** - Run setup-autostart.bat (one-time setup)
2. **Restart Windows** - LLM Hub will start automatically on login
3. **Zero Manual Steps** - Complete automation of the entire startup chain
4. **Predictive Maintenance** - Run start-health-monitor.bat for proactive issue prevention

## Documentation

### Getting Started
- [Installation Guide](docs/INSTALL.md) - Detailed setup instructions
- [Configuration](docs/CONFIGURATION.md) - Environment variables and settings
- [Troubleshooting](docs/TROUBLESHOOTING.md) - Common issues and solutions

### API Reference
- [MCP Endpoints](docs/api/MCP-ENDPOINTS.md) - Complete API documentation
- [Health Dashboard](docs/dashboard/) - Web-based monitoring interface

### Architecture & Development
- [System Overview](docs/architecture/OVERVIEW.md) - Architecture and design
- [Development Guide](docs/DEVELOPMENT.md) - Contributing and extending
- [ADR Index](docs/architecture/decisions/ADR-INDEX.md) - Architecture decisions

### Project Information
- [Changelog](CHANGELOG.md) - Release history and changes
- [Contributing](CONTRIBUTING.md) - How to contribute
- [License](LICENSE) - Project license

---

*For detailed examples and advanced usage, see the [documentation](docs/) directory.*
