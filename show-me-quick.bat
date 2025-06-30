@echo off
REM Quick "Show Me!" Test - Minimal output for CI/automation

echo Quick LLM Hub Test
echo ==================

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found
    exit /b 1
)

REM Install packages if needed
python -c "import requests" >nul 2>&1
if errorlevel 1 (
    pip install requests >nul 2>&1
)

REM Run tests with minimal output
cd ops\testing
python test_runner.py --style minimal --quiet

REM Exit with test result
exit /b %errorlevel%
