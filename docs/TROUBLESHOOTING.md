# LLM Hub Troubleshooting Guide

This guide helps resolve common issues when running LLM Hub on Windows.

## Common Issues

### Port 8080 Already in Use

**Problem:** Gateway fails to start with "port already in use" error.

**Solution:**
1. Check what's using port 8080:
   ```cmd
   netstat -ano | findstr :8080
   ```
2. Stop the conflicting process or change the gateway port:
   ```cmd
   set GATEWAY_PORT=8081
   ```
3. Restart the services

### Docker Not Running

**Problem:** `docker-compose up` fails with "Cannot connect to Docker daemon".

**Solution:**
1. Start Docker Desktop from Windows Start Menu
2. Wait for Docker to fully initialize (whale icon in system tray)
3. Verify Docker is running:
   ```cmd
   docker version
   ```
4. Restart LLM Hub with `start.bat`

### Service Unhealthy Status

**Problem:** Services show as "unhealthy" in Docker status.

**Solution:**
1. Check service logs:
   ```cmd
   docker-compose logs lm-studio-bridge
   docker-compose logs unified-gateway
   ```
2. Common causes:
   - LM Studio not running on port 1234
   - Missing environment variables
   - Network connectivity issues
3. Restart services:
   ```cmd
   docker-compose restart
   ```

### Connection Refused Errors

**Problem:** Services cannot connect to each other or LM Studio.

**Solution:**
1. Check Windows Firewall settings
2. Verify LM Studio is running and accessible:
   ```cmd
   curl http://localhost:1234/v1/models
   ```
3. Check Docker network:
   ```cmd
   docker network ls
   docker network inspect llm-hub-net
   ```
4. Restart Docker Desktop if network issues persist

### LM Studio Not Responding

**Problem:** Bridge cannot connect to LM Studio.

**Solution:**
1. Start LM Studio application
2. Load a model in LM Studio
3. Enable "Local Server" in LM Studio settings
4. Verify server is running on port 1234
5. Check LM Studio logs for errors

### Authentication Failures

**Problem:** API calls return 401 Unauthorized.

**Solution:**
1. Check API_KEY environment variable:
   ```cmd
   echo %API_KEY%
   ```
2. Update API key in `.env` file:
   ```
   API_KEY=your_secure_key_here
   ```
3. Restart services to pick up new environment

### Memory Issues

**Problem:** Services crash with out-of-memory errors.

**Solution:**
1. Increase Docker memory limit in Docker Desktop settings
2. Close unnecessary applications
3. Check available system memory:
   ```cmd
   wmic OS get TotalVisibleMemorySize,FreePhysicalMemory /value
   ```
4. Consider using smaller models in LM Studio

### Slow Response Times

**Problem:** API responses are very slow.

**Solution:**
1. Check system resources (CPU, memory, disk)
2. Verify LM Studio model is loaded and ready
3. Check Docker container resource limits
4. Consider using GPU acceleration in LM Studio
5. Reduce model size or context length

### Container Build Failures

**Problem:** Docker build fails during startup.

**Solution:**
1. Check internet connection for downloading dependencies
2. Clear Docker build cache:
   ```cmd
   docker system prune -a
   ```
3. Rebuild containers:
   ```cmd
   docker-compose build --no-cache
   ```
4. Check disk space availability

### Windows-Specific Issues

#### WSL2 Backend Issues
**Problem:** Docker Desktop WSL2 backend errors.

**Solution:**
1. Update WSL2:
   ```cmd
   wsl --update
   ```
2. Restart WSL2:
   ```cmd
   wsl --shutdown
   ```
3. Restart Docker Desktop

#### Antivirus Interference
**Problem:** Antivirus blocks Docker or network connections.

**Solution:**
1. Add Docker Desktop to antivirus exclusions
2. Add project directory to exclusions
3. Temporarily disable real-time protection for testing

#### Path Length Limitations
**Problem:** Build fails due to Windows path length limits.

**Solution:**
1. Move project to shorter path (e.g., `C:\llm-hub`)
2. Enable long path support in Windows:
   ```cmd
   reg add HKLM\SYSTEM\CurrentControlSet\Control\FileSystem /v LongPathsEnabled /t REG_DWORD /d 1
   ```

## Diagnostic Commands

### Check Service Status
```cmd
docker-compose ps
docker-compose logs --tail=50
```

### Test Connectivity
```cmd
curl http://localhost:8080/health
curl http://localhost:3000/health
curl http://localhost:1234/v1/models
```

### Check Resource Usage
```cmd
docker stats
docker system df
```

### Network Diagnostics
```cmd
docker network ls
netstat -ano | findstr :8080
netstat -ano | findstr :3000
netstat -ano | findstr :1234
```

## Getting Help

If these solutions don't resolve your issue:

1. Check the logs for specific error messages
2. Search existing issues in the project repository
3. Create a new issue with:
   - Operating system version
   - Docker Desktop version
   - Complete error messages
   - Steps to reproduce
   - Log outputs

## Prevention Tips

1. Always start LM Studio before running `start.bat`
2. Ensure Docker Desktop is running and healthy
3. Keep Docker Desktop and Windows updated
4. Monitor system resources during operation
5. Use the test scripts to verify functionality after changes
