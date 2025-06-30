@echo off
REM LLM Hub Autostart Setup Script
REM Configures Windows Task Scheduler for automatic startup

echo LLM Hub Autostart Setup
echo =======================

REM Check if running as administrator (not required, but recommended)
net session >nul 2>&1
if errorlevel 1 (
    echo NOTE: Running without administrator privileges
    echo This is fine, but autostart will only work for the current user
    echo.
)

REM Get current directory
set CURRENT_DIR=%~dp0
set CURRENT_DIR=%CURRENT_DIR:~0,-1%

echo Current LLM Hub directory: %CURRENT_DIR%
echo.

REM Update the XML file with the correct path
set XML_FILE=%CURRENT_DIR%\ops\autostart\llm-hub-autostart.xml
set TEMP_XML=%TEMP%\llm-hub-autostart-temp.xml

if not exist "%XML_FILE%" (
    echo ERROR: Autostart XML file not found at %XML_FILE%
    echo Please ensure you're running this from the LLM Hub root directory
    pause
    exit /b 1
)

echo Updating autostart configuration with current path...
powershell -Command "(Get-Content '%XML_FILE%') -replace '%%USERPROFILE%%\\Documents\\GitHub\\llm-hub', '%CURRENT_DIR%' | Set-Content '%TEMP_XML%'"

REM Register the task with Windows Task Scheduler
echo Registering autostart task with Windows Task Scheduler...
schtasks /create /tn "LLM Hub Autostart" /xml "%TEMP_XML%" /f

if errorlevel 1 (
    echo ERROR: Failed to register autostart task
    echo Please check Windows Task Scheduler permissions
    del "%TEMP_XML%" 2>nul
    pause
    exit /b 1
)

REM Clean up temporary file
del "%TEMP_XML%" 2>nul

echo ✓ Autostart task registered successfully
echo.
echo The following autostart chain is now configured:
echo 1. Windows startup → Task Scheduler (30 second delay)
echo 2. Task Scheduler → Docker Desktop startup wait
echo 3. Docker Desktop → LM Studio auto-launch
echo 4. LM Studio → LLM Hub services startup
echo.
echo To disable autostart:
echo   schtasks /delete /tn "LLM Hub Autostart" /f
echo.
echo To test autostart now:
echo   schtasks /run /tn "LLM Hub Autostart"
echo.
echo ✓ Setup complete! LLM Hub will start automatically on next login.

pause
