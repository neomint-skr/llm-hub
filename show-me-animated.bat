@echo off
REM "Show Me!" Test with Full Animations

echo.
echo 🎬 LLM Hub "Show Me!" Test - Animated Edition
echo =============================================
echo.
echo This will run tests with full animations and visual effects.
echo Perfect for demonstrations and presentations!
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ ERROR: Python is not installed
    pause
    exit /b 1
)

REM Install packages
python -c "import requests, asyncio" >nul 2>&1
if errorlevel 1 (
    echo 📦 Installing required packages...
    pip install requests
)

echo ✅ Starting animated test experience...
echo.

REM Run tests with animated style
cd ops\testing
python test_runner.py --style animated --verbose

pause
