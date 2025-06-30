@echo off
REM LLM Hub Windows Stop Script
REM Gracefully stops all services

echo Stopping LLM Hub...
echo ===================

REM Change to compose directory
cd ops\compose
if errorlevel 1 (
    echo ERROR: Could not change to ops\compose directory
    pause
    exit /b 1
)

echo Stopping services...
docker-compose down
if errorlevel 1 (
    echo WARNING: Some services may not have stopped cleanly
    echo Check with: docker ps
) else (
    echo ✓ All services stopped successfully
)

REM Return to root directory
cd ..\..

echo ===================
echo ✓ LLM Hub Stopped
echo ===================

pause
