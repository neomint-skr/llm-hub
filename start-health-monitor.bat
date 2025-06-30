@echo off
REM LLM Hub Health Monitor Startup Script
REM Starts predictive maintenance monitoring

echo LLM Hub Health Monitor
echo =======================

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)

echo ✓ Python is available

REM Check if required packages are installed
python -c "import psutil, asyncio" >nul 2>&1
if errorlevel 1 (
    echo Installing required packages...
    pip install psutil
    if errorlevel 1 (
        echo ERROR: Failed to install required packages
        pause
        exit /b 1
    )
)

echo ✓ Required packages are available

REM Start the Health Monitor
echo.
echo 🔮 Starting LLM Hub Health Monitor...
echo 📊 Dashboard: units\health-monitor\dashboard.html
echo ⚡ Monitoring system resources and predicting issues...
echo.
echo Press Ctrl+C to stop the monitor
echo.

cd units\health-monitor
python start_monitoring.py
