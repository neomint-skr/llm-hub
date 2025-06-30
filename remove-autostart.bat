@echo off
REM LLM Hub Autostart Removal Script
REM Removes Windows Task Scheduler autostart configuration

echo LLM Hub Autostart Removal
echo =========================

echo Removing autostart task from Windows Task Scheduler...

REM Check if task exists
schtasks /query /tn "LLM Hub Autostart" >nul 2>&1
if errorlevel 1 (
    echo No autostart task found - nothing to remove
    echo ✓ Autostart is already disabled
    pause
    exit /b 0
)

REM Remove the task
schtasks /delete /tn "LLM Hub Autostart" /f

if errorlevel 1 (
    echo ERROR: Failed to remove autostart task
    echo Please check Windows Task Scheduler permissions
    pause
    exit /b 1
)

echo ✓ Autostart task removed successfully
echo.
echo LLM Hub will no longer start automatically on Windows startup.
echo.
echo To re-enable autostart, run: setup-autostart.bat

pause
