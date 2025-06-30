@echo off
REM LLM Hub Windows Autostart Script
REM Complete autostart chain: Windows → Docker → LM Studio → Services

echo Starting LLM Hub Autostart Chain...
echo ===================================

REM Set autostart mode if called with /autostart parameter
set AUTOSTART_MODE=false
if "%1"=="/autostart" set AUTOSTART_MODE=true

REM Wait for Docker Desktop to start (up to 5 minutes)
echo Waiting for Docker Desktop to start...
set /a docker_wait=0
set /a max_docker_wait=60

:docker_wait_loop
docker version >nul 2>&1
if not errorlevel 1 goto docker_ready

if %docker_wait% geq %max_docker_wait% (
    echo ERROR: Docker Desktop did not start within 5 minutes
    if "%AUTOSTART_MODE%"=="false" pause
    exit /b 1
)

set /a docker_wait+=1
echo   Waiting for Docker Desktop... (%docker_wait%/%max_docker_wait%)
timeout /t 5 /nobreak >nul
goto docker_wait_loop

:docker_ready
echo ✓ Docker Desktop is running

REM Auto-start LM Studio if not running
echo Checking LM Studio status...
curl -s http://localhost:1234/v1/models >nul 2>&1
if errorlevel 1 (
    echo LM Studio not running, attempting to start...
    call :start_lm_studio
) else (
    echo ✓ LM Studio is already running
)

REM Check if port 8080 is available
netstat -an | findstr :8080 | findstr LISTENING >nul 2>&1
if not errorlevel 1 (
    echo WARNING: Port 8080 is already in use
    if "%AUTOSTART_MODE%"=="true" (
        echo Autostart mode: Continuing anyway
    ) else (
        echo Please stop the service using port 8080 or change GATEWAY_PORT in .env
        echo You can continue anyway, but the gateway may not start properly
        echo.
        set /p continue="Continue anyway? (y/N): "
        if /i not "%continue%"=="y" (
            echo Startup cancelled
            pause
            exit /b 1
        )
    )
)

echo ✓ Port 8080 appears to be available

REM Check if .env file exists, if not copy from example
if not exist "ops\compose\.env" (
    if exist "ops\compose\.env.example" (
        echo Creating .env file from .env.example...
        copy "ops\compose\.env.example" "ops\compose\.env" >nul
        echo ✓ .env file created
        echo Please edit ops\compose\.env with your configuration
    ) else (
        echo WARNING: No .env.example file found
    )
) else (
    echo ✓ .env file exists
)

REM Change to compose directory
cd ops\compose
if errorlevel 1 (
    echo ERROR: Could not change to ops\compose directory
    if "%AUTOSTART_MODE%"=="false" pause
    exit /b 1
)

echo Starting services with Docker Compose...
docker-compose up -d
if errorlevel 1 (
    echo ERROR: Failed to start services
    echo Check the logs with: docker-compose logs
    cd ..\..
    pause
    exit /b 1
)

echo ✓ Services started successfully

REM Wait for services to become healthy
echo Waiting for services to become healthy...
set /a counter=0
set /a max_wait=12

:wait_loop
if %counter% geq %max_wait% (
    echo WARNING: Services did not become healthy within 60 seconds
    goto show_status
)

docker inspect --format="{{.State.Health.Status}}" lm-studio-bridge 2>nul | findstr healthy >nul
if errorlevel 1 (
    set /a counter+=1
    echo   Waiting for services... (%counter%/%max_wait%)
    timeout /t 5 /nobreak >nul
    goto wait_loop
)

docker inspect --format="{{.State.Health.Status}}" unified-gateway 2>nul | findstr healthy >nul
if errorlevel 1 (
    set /a counter+=1
    echo   Waiting for services... (%counter%/%max_wait%)
    timeout /t 5 /nobreak >nul
    goto wait_loop
)

echo ✓ All services are healthy

:show_status
echo.
echo ==================
echo ✓ LLM Hub Started Successfully!
echo ==================
echo.
echo Gateway URL:      http://localhost:8080
echo Health Check:     http://localhost:8080/health
echo LM Studio URL:    http://localhost:1234
echo.
if "%AUTOSTART_MODE%"=="false" (
    echo Next Steps:
    echo 1. Make sure LM Studio is running on port 1234
    echo 2. Load a model in LM Studio
    echo 3. Test the gateway at http://localhost:8080/health
    echo 4. Use the API with your configured API key
    echo.
    echo To stop services: run stop.bat
    echo To view logs: run logs.bat
    echo ==================
)

REM Return to root directory
cd ..\..

if "%AUTOSTART_MODE%"=="false" pause
goto :eof

REM Function to start LM Studio
:start_lm_studio
echo Attempting to start LM Studio...
set LM_STUDIO_PATH=""

REM Try common LM Studio installation paths
if exist "%LOCALAPPDATA%\Programs\LM Studio\LM Studio.exe" (
    set LM_STUDIO_PATH="%LOCALAPPDATA%\Programs\LM Studio\LM Studio.exe"
) else if exist "%PROGRAMFILES%\LM Studio\LM Studio.exe" (
    set LM_STUDIO_PATH="%PROGRAMFILES%\LM Studio\LM Studio.exe"
) else if exist "%PROGRAMFILES(X86)%\LM Studio\LM Studio.exe" (
    set LM_STUDIO_PATH="%PROGRAMFILES(X86)%\LM Studio\LM Studio.exe"
)

if %LM_STUDIO_PATH%=="" (
    echo WARNING: LM Studio not found in common installation paths
    echo Please start LM Studio manually and ensure it's running on port 1234
    if "%AUTOSTART_MODE%"=="false" pause
    goto :eof
)

echo Starting LM Studio from %LM_STUDIO_PATH%
start "" %LM_STUDIO_PATH%

REM Wait for LM Studio to start (up to 2 minutes)
echo Waiting for LM Studio to start...
set /a lm_wait=0
set /a max_lm_wait=24

:lm_wait_loop
curl -s http://localhost:1234/v1/models >nul 2>&1
if not errorlevel 1 (
    echo ✓ LM Studio is now running
    goto :eof
)

if %lm_wait% geq %max_lm_wait% (
    echo WARNING: LM Studio did not start within 2 minutes
    echo Please check LM Studio manually and ensure it's configured for port 1234
    goto :eof
)

set /a lm_wait+=1
echo   Waiting for LM Studio... (%lm_wait%/%max_lm_wait%)
timeout /t 5 /nobreak >nul
goto lm_wait_loop
