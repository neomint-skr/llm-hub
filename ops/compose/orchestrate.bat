@echo off
REM LLM Hub Perfect Orchestration Script for Windows
REM Implements 4D Methodology: GUTWILLIG, INTELLIGENT, KONTEXT-AWARE, FAUL
REM Provides startup sequencing, health validation, and graceful shutdown

setlocal enabledelayedexpansion

REM Configuration
set SCRIPT_DIR=%~dp0
set LOG_DIR=%SCRIPT_DIR%logs
set COMPOSE_FILE=%SCRIPT_DIR%docker-compose.yml
set SHARED_STATE_DIR=%LOG_DIR%\shared-state

REM Create log directories
if not exist "%LOG_DIR%\orchestration" mkdir "%LOG_DIR%\orchestration"
if not exist "%LOG_DIR%\bridge" mkdir "%LOG_DIR%\bridge"
if not exist "%LOG_DIR%\gateway" mkdir "%LOG_DIR%\gateway"
if not exist "%SHARED_STATE_DIR%" mkdir "%SHARED_STATE_DIR%"

REM Initialize log file
echo. > "%LOG_DIR%\orchestration\orchestrate.log"

REM Logging functions
:log_info
echo [INFO] %~1
echo [%date% %time%] [INFO] %~1 >> "%LOG_DIR%\orchestration\orchestrate.log"
goto :eof

:log_success
echo [SUCCESS] %~1
echo [%date% %time%] [SUCCESS] %~1 >> "%LOG_DIR%\orchestration\orchestrate.log"
goto :eof

:log_warning
echo [WARNING] %~1
echo [%date% %time%] [WARNING] %~1 >> "%LOG_DIR%\orchestration\orchestrate.log"
goto :eof

:log_error
echo [ERROR] %~1
echo [%date% %time%] [ERROR] %~1 >> "%LOG_DIR%\orchestration\orchestrate.log"
goto :eof

:log_phase
echo [PHASE] %~1
echo [%date% %time%] [PHASE] %~1 >> "%LOG_DIR%\orchestration\orchestrate.log"
goto :eof

REM Main orchestration logic
set COMMAND=%1
if "%COMMAND%"=="" set COMMAND=help

call :log_info "🚀 LLM Hub Perfect Orchestration Starting..."
call :log_info "📁 Log directory: %LOG_DIR%"
call :log_info "🐳 Compose file: %COMPOSE_FILE%"

if "%COMMAND%"=="start" goto start_services
if "%COMMAND%"=="stop" goto stop_services
if "%COMMAND%"=="restart" goto restart_services
if "%COMMAND%"=="status" goto show_status
if "%COMMAND%"=="logs" goto show_logs
goto show_help

:start_services
call :log_info "🚀 LLM Hub Perfect Orchestration Starting..."
call :log_info "📁 Log directory: %LOG_DIR%"
call :log_info "🐳 Compose file: %COMPOSE_FILE%"

REM Validate prerequisites
call :log_phase "🔍 Phase 0: Prerequisites Validation"

REM Check Docker
docker --version >nul 2>&1
if errorlevel 1 (
    call :log_error "Docker is not installed or not in PATH"
    exit /b 1
)

REM Check Docker Compose
docker-compose --version >nul 2>&1
if errorlevel 1 (
    call :log_error "Docker Compose is not installed or not in PATH"
    exit /b 1
)

REM Check Docker daemon
docker info >nul 2>&1
if errorlevel 1 (
    call :log_error "Docker daemon is not running"
    exit /b 1
)

REM Check compose file
if not exist "%COMPOSE_FILE%" (
    call :log_error "Docker Compose file not found: %COMPOSE_FILE%"
    exit /b 1
)

call :log_success "✅ All prerequisites validated"

REM Check for existing services
call :log_info "🔍 Checking for existing services..."
docker ps --format "table {{.Names}}" | findstr "lm-studio-bridge" >nul 2>&1
if not errorlevel 1 (
    call :log_warning "Found running lm-studio-bridge service"
    call :log_info "Use 'orchestrate.bat stop' to stop existing services first"
    exit /b 1
)

docker ps --format "table {{.Names}}" | findstr "unified-gateway" >nul 2>&1
if not errorlevel 1 (
    call :log_warning "Found running unified-gateway service"
    call :log_info "Use 'orchestrate.bat stop' to stop existing services first"
    exit /b 1
)

call :log_success "✅ No conflicting services found"

REM Phase 1: Infrastructure
call :log_phase "🔧 Phase 1: Infrastructure Validation"
call :log_info "Starting infrastructure check..."
docker-compose -f "%COMPOSE_FILE%" up -d infrastructure-check
if errorlevel 1 (
    call :log_error "Failed to start infrastructure check"
    exit /b 1
)

call :wait_for_service_health "llm-hub-infrastructure-check" 30
if errorlevel 1 (
    call :log_error "Infrastructure validation failed"
    exit /b 1
)

REM Phase 2: LM Studio Bridge
call :log_phase "🌉 Phase 2: LM Studio Bridge"
call :log_info "Starting LM Studio Bridge..."
docker-compose -f "%COMPOSE_FILE%" up -d lm-studio-bridge
if errorlevel 1 (
    call :log_error "Failed to start LM Studio Bridge"
    exit /b 1
)

call :wait_for_service_health "lm-studio-bridge" 90
if errorlevel 1 (
    call :log_error "LM Studio Bridge startup failed"
    call :show_service_logs "lm-studio-bridge"
    exit /b 1
)

REM Validate Bridge readiness
call :validate_service_readiness "lm-studio-bridge" "http://localhost:3000/health"
if errorlevel 1 (
    call :log_error "LM Studio Bridge readiness validation failed"
    exit /b 1
)

REM Phase 3: Unified Gateway
call :log_phase "🚪 Phase 3: Unified Gateway"
call :log_info "Starting Unified Gateway..."
docker-compose -f "%COMPOSE_FILE%" up -d unified-gateway
if errorlevel 1 (
    call :log_error "Failed to start Unified Gateway"
    exit /b 1
)

call :wait_for_service_health "unified-gateway" 75
if errorlevel 1 (
    call :log_error "Unified Gateway startup failed"
    call :show_service_logs "unified-gateway"
    exit /b 1
)

REM Validate Gateway readiness
call :validate_service_readiness "unified-gateway" "http://localhost:8080/health"
if errorlevel 1 (
    call :log_error "Unified Gateway readiness validation failed"
    exit /b 1
)

REM Phase 4: Orchestration Monitor
call :log_phase "🔍 Phase 4: Orchestration Monitor"
call :log_info "Starting orchestration monitor..."
docker-compose -f "%COMPOSE_FILE%" up -d orchestration-monitor
if errorlevel 1 (
    call :log_warning "Failed to start orchestration monitor (non-critical)"
) else (
    call :wait_for_service_health "llm-hub-orchestration-monitor" 30
    if errorlevel 1 (
        call :log_warning "Orchestration monitor startup failed (non-critical)"
    )
)

call :log_success "🎉 All services started successfully!"
call :show_final_status
goto :eof

:stop_services
call :log_phase "🛑 Graceful Shutdown Starting"
call :log_info "Stopping services in reverse dependency order..."

REM Stop in reverse order
call :log_info "Stopping orchestration-monitor..."
docker-compose -f "%COMPOSE_FILE%" stop orchestration-monitor 2>nul

call :log_info "Stopping unified-gateway..."
docker-compose -f "%COMPOSE_FILE%" stop unified-gateway 2>nul

call :log_info "Stopping lm-studio-bridge..."
docker-compose -f "%COMPOSE_FILE%" stop lm-studio-bridge 2>nul

call :log_info "Stopping infrastructure-check..."
docker-compose -f "%COMPOSE_FILE%" stop infrastructure-check 2>nul

call :log_info "Removing containers..."
docker-compose -f "%COMPOSE_FILE%" down --remove-orphans

call :log_success "✅ Graceful shutdown complete"
goto :eof

:restart_services
call :stop_services
timeout /t 2 /nobreak >nul
call :start_services
goto :eof

:show_status
echo LLM Hub Service Status:
echo ======================

REM Check each service
set services=llm-hub-infrastructure-check lm-studio-bridge unified-gateway llm-hub-orchestration-monitor

for %%s in (%services%) do (
    docker ps --format "table {{.Names}}" | findstr "%%s" >nul 2>&1
    if not errorlevel 1 (
        for /f "tokens=*" %%h in ('docker inspect --format="{{.State.Health.Status}}" "%%s" 2^>nul') do (
            echo   • %%s: RUNNING (%%h)
        )
    ) else (
        echo   • %%s: STOPPED
    )
)

echo.
echo Network Status:
docker network ls | findstr "llm-hub-network" >nul 2>&1
if not errorlevel 1 (
    echo   • llm-hub-network: EXISTS
) else (
    echo   • llm-hub-network: NOT_FOUND
)

echo.
echo Volume Status:
docker volume ls | findstr "llm-hub-logs" >nul 2>&1
if not errorlevel 1 (
    echo   • llm-hub-logs: EXISTS
) else (
    echo   • llm-hub-logs: NOT_FOUND
)
goto :eof

:show_logs
if "%2"=="" (
    echo Usage: %0 logs ^<service_name^> [lines]
    echo Available services: infrastructure-check, lm-studio-bridge, unified-gateway, orchestration-monitor
    goto :eof
)

set lines=%3
if "%lines%"=="" set lines=50

call :log_info "📋 Last %lines% lines of %2 logs:"
echo ----------------------------------------
docker-compose -f "%COMPOSE_FILE%" logs --tail="%lines%" "%2"
echo ----------------------------------------
goto :eof

:wait_for_service_health
set service_name=%1
set timeout=%2
if "%timeout%"=="" set timeout=120
set elapsed=0
set interval=5

call :log_info "⏳ Waiting for %service_name% to become healthy (timeout: %timeout%s)..."

:wait_loop
if %elapsed% geq %timeout% (
    call :log_error "❌ %service_name% did not become healthy within %timeout%s"
    exit /b 1
)

for /f "tokens=*" %%h in ('docker inspect --format="{{.State.Health.Status}}" "%service_name%" 2^>nul') do set health_status=%%h

if "%health_status%"=="healthy" (
    call :log_success "✅ %service_name% is healthy (%elapsed%s)"
    exit /b 0
)

if "%health_status%"=="unhealthy" (
    call :log_warning "⚠️  %service_name% is unhealthy, continuing to wait..."
) else if "%health_status%"=="starting" (
    call :log_info "🔄 %service_name% is starting..."
) else (
    call :log_info "🔄 %service_name% status: %health_status%"
)

timeout /t %interval% /nobreak >nul
set /a elapsed+=%interval%

REM Show progress every 15 seconds
set /a progress_check=%elapsed% %% 15
if %progress_check%==0 (
    call :log_info "⏳ Still waiting for %service_name%... (%elapsed%/%timeout%s)"
)

goto wait_loop

:validate_service_readiness
set service_name=%1
set health_url=%2

call :log_info "🔍 Validating %service_name% readiness..."

REM Check HTTP health endpoint
curl -sf "%health_url%" >nul 2>&1
if errorlevel 1 (
    call :log_error "❌ %service_name% HTTP health check failed"
    exit /b 1
)

call :log_success "✅ %service_name% HTTP health check passed"
exit /b 0

:show_service_logs
set service_name=%1
set lines=%2
if "%lines%"=="" set lines=50

call :log_info "📋 Last %lines% lines of %service_name% logs:"
echo ----------------------------------------
docker-compose -f "%COMPOSE_FILE%" logs --tail="%lines%" "%service_name%"
echo ----------------------------------------
goto :eof

:show_final_status
echo.
echo 🎯 LLM Hub Orchestration Complete!
echo ==================================
echo.
echo 🌐 Service URLs:
echo   • Gateway:       http://localhost:8080
echo   • Health:        http://localhost:8080/health
echo   • Bridge:        http://localhost:3000
echo   • Bridge Health: http://localhost:3000/health
echo.
echo 📊 Service Status:

set services=llm-hub-infrastructure-check lm-studio-bridge unified-gateway llm-hub-orchestration-monitor

for %%s in (%services%) do (
    for /f "tokens=*" %%h in ('docker inspect --format="{{.State.Health.Status}}" "%%s" 2^>nul') do (
        if "%%h"=="healthy" (
            echo   • %%s: ✅ HEALTHY
        ) else if "%%h"=="unhealthy" (
            echo   • %%s: ❌ UNHEALTHY
        ) else if "%%h"=="starting" (
            echo   • %%s: 🔄 STARTING
        ) else (
            echo   • %%s: ⚠️  %%h
        )
    )
)

echo.
echo 📁 Logs: %LOG_DIR%
echo 🛑 Stop: orchestrate.bat stop
echo 📊 Status: orchestrate.bat status
echo ==================================
goto :eof

:show_help
echo LLM Hub Perfect Orchestration
echo Usage: %0 {start^|stop^|restart^|status^|logs}
echo.
echo Commands:
echo   start    - Start all services with perfect orchestration
echo   stop     - Gracefully stop all services
echo   restart  - Stop and start all services
echo   status   - Show current service status
echo   logs     - Show service logs
echo.
echo Examples:
echo   %0 start
echo   %0 logs lm-studio-bridge 50
echo   %0 status
goto :eof
