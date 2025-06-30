@echo off
REM LLM Hub Windows Logs Script
REM Shows container logs for debugging

echo LLM Hub Logs
echo =============
echo Press Ctrl+C to stop following logs
echo.

REM Change to compose directory
cd ops\compose
if errorlevel 1 (
    echo ERROR: Could not change to ops\compose directory
    pause
    exit /b 1
)

REM Show logs with follow and tail
docker-compose logs -f --tail=100

REM Return to root directory
cd ..\..

echo.
echo Logs stopped
pause
