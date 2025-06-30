@echo off
REM "Show Me!" Test Script for LLM Hub
REM Demonstrates that everything is working with visual feedback

echo.
echo 🚀 LLM Hub "Show Me!" Test
echo ==========================
echo.
echo This will demonstrate that LLM Hub is working correctly
echo with clear visual feedback for each component.
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)

echo ✅ Python is available

REM Check if required packages are installed
python -c "import requests, asyncio" >nul 2>&1
if errorlevel 1 (
    echo 📦 Installing required packages...
    pip install requests
    if errorlevel 1 (
        echo ❌ ERROR: Failed to install required packages
        pause
        exit /b 1
    )
    echo ✅ Required packages installed
)

echo ✅ Required packages are available
echo.

REM Ask user for visual style preference
echo 🎨 Choose visual style:
echo   1. Standard (recommended)
echo   2. Rich (detailed information)
echo   3. Animated (full animations)
echo   4. Minimal (simple text)
echo.
set /p style_choice="Enter choice (1-4, default 1): "

REM Set visual style based on choice
set visual_style=standard
if "%style_choice%"=="2" set visual_style=rich
if "%style_choice%"=="3" set visual_style=animated
if "%style_choice%"=="4" set visual_style=minimal

echo.
echo 🔄 Running "Show Me!" tests with %visual_style% visuals...
echo.

cd ops\testing
python test_runner.py --style %visual_style%

REM Check the exit code
if errorlevel 1 (
    echo.
    echo ❌ Some tests failed. Please check the output above.
    echo.
    echo 💡 Common solutions:
    echo    • Make sure Docker Desktop is running
    echo    • Run start.bat to start LLM Hub services
    echo    • Check that LM Studio is running on port 1234
    echo.
    pause
    exit /b 1
) else (
    echo.
    echo 🎉 All tests passed! LLM Hub is working correctly.
    echo.
    echo 🚀 Your LLM Hub is ready to use:
    echo    • Gateway: http://localhost:8080
    echo    • Health Dashboard: http://localhost:8080/health
    echo    • Control Center: http://localhost:9000
    echo.
)

pause
