#!/bin/bash
# LLM Hub Perfect Orchestration Script
# Implements 4D Methodology: GUTWILLIG, INTELLIGENT, KONTEXT-AWARE, FAUL
# Provides startup sequencing, health validation, and graceful shutdown

set -euo pipefail

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_DIR="${SCRIPT_DIR}/logs"
COMPOSE_FILE="${SCRIPT_DIR}/docker-compose.yml"
SHARED_STATE_DIR="${LOG_DIR}/shared-state"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Logging functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1" | tee -a "${LOG_DIR}/orchestration/orchestrate.log"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1" | tee -a "${LOG_DIR}/orchestration/orchestrate.log"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1" | tee -a "${LOG_DIR}/orchestration/orchestrate.log"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1" | tee -a "${LOG_DIR}/orchestration/orchestrate.log"
}

log_phase() {
    echo -e "${PURPLE}[PHASE]${NC} $1" | tee -a "${LOG_DIR}/orchestration/orchestrate.log"
}

# Initialize logging
init_logging() {
    mkdir -p "${LOG_DIR}/orchestration" "${LOG_DIR}/bridge" "${LOG_DIR}/gateway"
    mkdir -p "${SHARED_STATE_DIR}"
    
    # Clear previous orchestration logs
    > "${LOG_DIR}/orchestration/orchestrate.log"
    
    log_info "🚀 LLM Hub Perfect Orchestration Starting..."
    log_info "📁 Log directory: ${LOG_DIR}"
    log_info "🐳 Compose file: ${COMPOSE_FILE}"
    log_info "💾 Shared state: ${SHARED_STATE_DIR}"
}

# Validate prerequisites
validate_prerequisites() {
    log_phase "🔍 Phase 0: Prerequisites Validation"
    
    # Check Docker
    if ! command -v docker &> /dev/null; then
        log_error "Docker is not installed or not in PATH"
        exit 1
    fi
    
    # Check Docker Compose
    if ! command -v docker-compose &> /dev/null; then
        log_error "Docker Compose is not installed or not in PATH"
        exit 1
    fi
    
    # Check Docker daemon
    if ! docker info &> /dev/null; then
        log_error "Docker daemon is not running"
        exit 1
    fi
    
    # Check compose file
    if [[ ! -f "$COMPOSE_FILE" ]]; then
        log_error "Docker Compose file not found: $COMPOSE_FILE"
        exit 1
    fi
    
    # Validate compose file
    if ! docker-compose -f "$COMPOSE_FILE" config &> /dev/null; then
        log_error "Invalid Docker Compose configuration"
        exit 1
    fi
    
    log_success "✅ All prerequisites validated"
}

# Check if services are already running
check_existing_services() {
    log_info "🔍 Checking for existing services..."
    
    local running_services=()
    
    if docker ps --format "table {{.Names}}" | grep -q "lm-studio-bridge"; then
        running_services+=("lm-studio-bridge")
    fi
    
    if docker ps --format "table {{.Names}}" | grep -q "unified-gateway"; then
        running_services+=("unified-gateway")
    fi
    
    if [[ ${#running_services[@]} -gt 0 ]]; then
        log_warning "Found running services: ${running_services[*]}"
        log_info "Use './orchestrate.sh stop' to stop existing services first"
        return 1
    fi
    
    log_success "✅ No conflicting services found"
    return 0
}

# Wait for service health with timeout
wait_for_service_health() {
    local service_name="$1"
    local timeout="${2:-120}"
    local interval="${3:-5}"
    local elapsed=0
    
    log_info "⏳ Waiting for $service_name to become healthy (timeout: ${timeout}s)..."
    
    while [[ $elapsed -lt $timeout ]]; do
        local health_status
        health_status=$(docker inspect --format="{{.State.Health.Status}}" "$service_name" 2>/dev/null || echo "not_found")
        
        case "$health_status" in
            "healthy")
                log_success "✅ $service_name is healthy (${elapsed}s)"
                return 0
                ;;
            "unhealthy")
                log_warning "⚠️  $service_name is unhealthy, continuing to wait..."
                ;;
            "starting")
                log_info "🔄 $service_name is starting..."
                ;;
            "not_found")
                log_warning "⚠️  $service_name container not found, waiting..."
                ;;
            *)
                log_info "🔄 $service_name status: $health_status"
                ;;
        esac
        
        sleep "$interval"
        elapsed=$((elapsed + interval))
        
        # Show progress
        if [[ $((elapsed % 15)) -eq 0 ]]; then
            log_info "⏳ Still waiting for $service_name... (${elapsed}/${timeout}s)"
        fi
    done
    
    log_error "❌ $service_name did not become healthy within ${timeout}s"
    return 1
}

# Validate service readiness
validate_service_readiness() {
    local service_name="$1"
    local health_url="$2"
    
    log_info "🔍 Validating $service_name readiness..."
    
    # Check HTTP health endpoint
    if curl -sf "$health_url" >/dev/null 2>&1; then
        local health_response
        health_response=$(curl -s "$health_url" | jq -r '.status' 2>/dev/null || echo "unknown")
        
        if [[ "$health_response" == "healthy" ]]; then
            log_success "✅ $service_name HTTP health check passed"
        else
            log_warning "⚠️  $service_name HTTP health status: $health_response"
        fi
    else
        log_error "❌ $service_name HTTP health check failed"
        return 1
    fi
    
    return 0
}

# Start services with perfect orchestration
start_services() {
    log_phase "🚀 Starting LLM Hub Services with Perfect Orchestration"
    
    # Phase 1: Infrastructure
    log_phase "🔧 Phase 1: Infrastructure Validation"
    log_info "Starting infrastructure check..."
    docker-compose -f "$COMPOSE_FILE" up -d infrastructure-check
    
    if ! wait_for_service_health "llm-hub-infrastructure-check" 30 2; then
        log_error "Infrastructure validation failed"
        return 1
    fi
    
    # Phase 2: LM Studio Bridge
    log_phase "🌉 Phase 2: LM Studio Bridge"
    log_info "Starting LM Studio Bridge..."
    docker-compose -f "$COMPOSE_FILE" up -d lm-studio-bridge
    
    if ! wait_for_service_health "lm-studio-bridge" 90 5; then
        log_error "LM Studio Bridge startup failed"
        show_service_logs "lm-studio-bridge"
        return 1
    fi
    
    # Validate Bridge readiness
    if ! validate_service_readiness "lm-studio-bridge" "http://localhost:3000/health"; then
        log_error "LM Studio Bridge readiness validation failed"
        return 1
    fi
    
    # Phase 3: Unified Gateway
    log_phase "🚪 Phase 3: Unified Gateway"
    log_info "Starting Unified Gateway..."
    docker-compose -f "$COMPOSE_FILE" up -d unified-gateway
    
    if ! wait_for_service_health "unified-gateway" 75 5; then
        log_error "Unified Gateway startup failed"
        show_service_logs "unified-gateway"
        return 1
    fi
    
    # Validate Gateway readiness
    if ! validate_service_readiness "unified-gateway" "http://localhost:8080/health"; then
        log_error "Unified Gateway readiness validation failed"
        return 1
    fi
    
    # Phase 4: Orchestration Monitor
    log_phase "🔍 Phase 4: Orchestration Monitor"
    log_info "Starting orchestration monitor..."
    docker-compose -f "$COMPOSE_FILE" up -d orchestration-monitor
    
    if ! wait_for_service_health "llm-hub-orchestration-monitor" 30 2; then
        log_warning "Orchestration monitor startup failed (non-critical)"
    fi
    
    log_success "🎉 All services started successfully!"
    return 0
}

# Show service logs for debugging
show_service_logs() {
    local service_name="$1"
    local lines="${2:-50}"
    
    log_info "📋 Last $lines lines of $service_name logs:"
    echo "----------------------------------------"
    docker-compose -f "$COMPOSE_FILE" logs --tail="$lines" "$service_name" || true
    echo "----------------------------------------"
}

# Display final status
show_final_status() {
    log_phase "📊 Final Status Report"
    
    echo ""
    echo "🎯 LLM Hub Orchestration Complete!"
    echo "=================================="
    echo ""
    echo "🌐 Service URLs:"
    echo "  • Gateway:     http://localhost:8080"
    echo "  • Health:      http://localhost:8080/health"
    echo "  • Bridge:      http://localhost:3000"
    echo "  • Bridge Health: http://localhost:3000/health"
    echo ""
    echo "📊 Service Status:"
    
    # Check each service
    local services=("llm-hub-infrastructure-check" "lm-studio-bridge" "unified-gateway" "llm-hub-orchestration-monitor")
    
    for service in "${services[@]}"; do
        local status
        status=$(docker inspect --format="{{.State.Health.Status}}" "$service" 2>/dev/null || echo "not_found")
        
        case "$status" in
            "healthy")
                echo "  • $service: ✅ HEALTHY"
                ;;
            "unhealthy")
                echo "  • $service: ❌ UNHEALTHY"
                ;;
            "starting")
                echo "  • $service: 🔄 STARTING"
                ;;
            *)
                echo "  • $service: ⚠️  $status"
                ;;
        esac
    done
    
    echo ""
    echo "📁 Logs: $LOG_DIR"
    echo "🛑 Stop: ./orchestrate.sh stop"
    echo "📊 Status: ./orchestrate.sh status"
    echo "=================================="
}

# Graceful shutdown
stop_services() {
    log_phase "🛑 Graceful Shutdown Starting"
    
    log_info "Stopping services in reverse dependency order..."
    
    # Stop in reverse order
    local services=("orchestration-monitor" "unified-gateway" "lm-studio-bridge" "infrastructure-check")
    
    for service in "${services[@]}"; do
        log_info "Stopping $service..."
        docker-compose -f "$COMPOSE_FILE" stop "$service" || true
    done
    
    log_info "Removing containers..."
    docker-compose -f "$COMPOSE_FILE" down --remove-orphans
    
    log_success "✅ Graceful shutdown complete"
}

# Show current status
show_status() {
    log_phase "📊 Current Status"
    
    echo "LLM Hub Service Status:"
    echo "======================"
    
    local services=("llm-hub-infrastructure-check" "lm-studio-bridge" "unified-gateway" "llm-hub-orchestration-monitor")
    
    for service in "${services[@]}"; do
        if docker ps --format "table {{.Names}}" | grep -q "$service"; then
            local status
            status=$(docker inspect --format="{{.State.Health.Status}}" "$service" 2>/dev/null || echo "no_health_check")
            echo "  • $service: RUNNING ($status)"
        else
            echo "  • $service: STOPPED"
        fi
    done
    
    echo ""
    echo "Network Status:"
    if docker network ls | grep -q "llm-hub-network"; then
        echo "  • llm-hub-network: EXISTS"
    else
        echo "  • llm-hub-network: NOT_FOUND"
    fi
    
    echo ""
    echo "Volume Status:"
    if docker volume ls | grep -q "llm-hub-logs"; then
        echo "  • llm-hub-logs: EXISTS"
    else
        echo "  • llm-hub-logs: NOT_FOUND"
    fi
}

# Main function
main() {
    local command="${1:-start}"
    
    case "$command" in
        "start")
            init_logging
            validate_prerequisites
            if check_existing_services; then
                if start_services; then
                    show_final_status
                    exit 0
                else
                    log_error "❌ Orchestration failed"
                    exit 1
                fi
            else
                exit 1
            fi
            ;;
        "stop")
            init_logging
            stop_services
            ;;
        "restart")
            init_logging
            stop_services
            sleep 2
            validate_prerequisites
            if start_services; then
                show_final_status
                exit 0
            else
                log_error "❌ Restart failed"
                exit 1
            fi
            ;;
        "status")
            show_status
            ;;
        "logs")
            local service="${2:-}"
            if [[ -n "$service" ]]; then
                show_service_logs "$service" "${3:-100}"
            else
                echo "Usage: $0 logs <service_name> [lines]"
                echo "Available services: infrastructure-check, lm-studio-bridge, unified-gateway, orchestration-monitor"
            fi
            ;;
        *)
            echo "LLM Hub Perfect Orchestration"
            echo "Usage: $0 {start|stop|restart|status|logs}"
            echo ""
            echo "Commands:"
            echo "  start    - Start all services with perfect orchestration"
            echo "  stop     - Gracefully stop all services"
            echo "  restart  - Stop and start all services"
            echo "  status   - Show current service status"
            echo "  logs     - Show service logs"
            echo ""
            echo "Examples:"
            echo "  $0 start"
            echo "  $0 logs lm-studio-bridge 50"
            echo "  $0 status"
            exit 1
            ;;
    esac
}

# Handle signals for graceful shutdown
trap 'log_warning "Received interrupt signal, stopping..."; stop_services; exit 130' INT TERM

# Run main function
main "$@"
