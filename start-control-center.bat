@echo off
REM LLM Hub Control Center Startup Script
REM Starts the control API and optionally the system tray

echo LLM Hub Control Center
echo ======================

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
python -c "import fastapi, uvicorn" >nul 2>&1
if errorlevel 1 (
    echo Installing required packages...
    pip install fastapi uvicorn
    if errorlevel 1 (
        echo ERROR: Failed to install required packages
        pause
        exit /b 1
    )
)

echo ✓ Required packages are available

REM Start the Control API server
echo Starting Control API server...
echo.
echo 🚀 Control Center will be available at: http://localhost:9000
echo 📊 API Documentation: http://localhost:9000/docs
echo.

REM Ask user if they want to start system tray
set /p start_tray="Start system tray integration? (y/N): "

if /i "%start_tray%"=="y" (
    echo.
    echo Starting system tray integration...
    
    REM Check if system tray packages are available
    python -c "import pystray, PIL" >nul 2>&1
    if errorlevel 1 (
        echo Installing system tray packages...
        pip install pystray pillow
        if errorlevel 1 (
            echo WARNING: Failed to install system tray packages
            echo System tray will not be available
            set start_tray=n
        )
    )
    
    if /i "%start_tray%"=="y" (
        echo ✓ System tray packages available
        echo.
        echo Starting both Control API and System Tray...
        echo Right-click the system tray icon for quick actions
        echo.
        
        REM Start system tray in background
        start /min python ops\control\system_tray.py
        
        REM Wait a moment for tray to start
        timeout /t 2 /nobreak >nul
    )
)

REM Start the Control API server (this will block)
cd ops\control
python control_api.py
