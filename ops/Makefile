# LLM Hub Makefile
# Common commands for build, test, and deployment

.PHONY: help install build test clean start stop restart logs health deploy docs lint format validate

# Default target
.DEFAULT_GOAL := help

# Variables
COMPOSE_FILE := ops/compose/docker-compose.yml
COMPOSE_PROD_FILE := ops/compose/docker-compose.prod.yml
PYTHON := python3
PIP := pip3

# Colors for output
BLUE := \033[36m
GREEN := \033[32m
YELLOW := \033[33m
RED := \033[31m
NC := \033[0m # No Color

help: ## Show this help message
	@echo "$(BLUE)LLM Hub Makefile$(NC)"
	@echo "=================="
	@echo ""
	@echo "$(GREEN)Available commands:$(NC)"
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  $(YELLOW)%-15s$(NC) %s\n", $$1, $$2}' $(MAKEFILE_LIST)

# =============================================================================
# INSTALLATION AND SETUP
# =============================================================================

install: ## Install development dependencies
	@echo "$(BLUE)Installing development dependencies...$(NC)"
	$(PIP) install --upgrade pip
	$(PIP) install httpx pytest black flake8 mypy isort bandit
	@echo "$(GREEN)Dependencies installed successfully$(NC)"

setup: ## Set up development environment
	@echo "$(BLUE)Setting up development environment...$(NC)"
	cp ops/compose/.env.example ops/compose/.env
	@echo "$(YELLOW)Please edit ops/compose/.env with your configuration$(NC)"
	@echo "$(GREEN)Development environment setup complete$(NC)"

# =============================================================================
# BUILD AND DEPLOYMENT
# =============================================================================

build: ## Build Docker images
	@echo "$(BLUE)Building Docker images...$(NC)"
	docker-compose -f $(COMPOSE_FILE) build
	@echo "$(GREEN)Build completed successfully$(NC)"

build-prod: ## Build production Docker images
	@echo "$(BLUE)Building production Docker images...$(NC)"
	docker-compose -f $(COMPOSE_PROD_FILE) build
	@echo "$(GREEN)Production build completed successfully$(NC)"

start: ## Start development services
	@echo "$(BLUE)Starting LLM Hub services...$(NC)"
	docker-compose -f $(COMPOSE_FILE) up -d
	@echo "$(GREEN)Services started successfully$(NC)"
	@echo "$(YELLOW)Gateway: http://localhost:8080$(NC)"
	@echo "$(YELLOW)Bridge: http://localhost:3000$(NC)"

start-prod: ## Start production services
	@echo "$(BLUE)Starting LLM Hub production services...$(NC)"
	docker-compose -f $(COMPOSE_PROD_FILE) up -d
	@echo "$(GREEN)Production services started successfully$(NC)"

stop: ## Stop all services
	@echo "$(BLUE)Stopping LLM Hub services...$(NC)"
	docker-compose -f $(COMPOSE_FILE) down
	docker-compose -f $(COMPOSE_PROD_FILE) down 2>/dev/null || true
	@echo "$(GREEN)Services stopped successfully$(NC)"

restart: stop start ## Restart all services

# =============================================================================
# TESTING
# =============================================================================

test: ## Run all tests
	@echo "$(BLUE)Running all tests...$(NC)"
	cd ops/scripts && bash run-all-tests.sh
	@echo "$(GREEN)All tests completed$(NC)"

test-unit: ## Run unit tests only
	@echo "$(BLUE)Running unit tests...$(NC)"
	find units -name "tests" -type d -exec $(PYTHON) -m pytest {} \; 2>/dev/null || echo "No unit tests found"
	@echo "$(GREEN)Unit tests completed$(NC)"

test-integration: ## Run integration tests
	@echo "$(BLUE)Running integration tests...$(NC)"
	cd ops/scripts && bash integration-test.sh
	@echo "$(GREEN)Integration tests completed$(NC)"

test-mcp: ## Run MCP compliance tests
	@echo "$(BLUE)Running MCP compliance tests...$(NC)"
	cd ops/scripts && bash mcp-compliance-test.sh
	@echo "$(GREEN)MCP compliance tests completed$(NC)"

# =============================================================================
# CODE QUALITY
# =============================================================================

lint: ## Run linting on all Python code
	@echo "$(BLUE)Running linting...$(NC)"
	find units -name "*.py" -exec flake8 {} \; || true
	find ops/scripts -name "*.py" -exec flake8 {} \; || true
	@echo "$(GREEN)Linting completed$(NC)"

format: ## Format all Python code
	@echo "$(BLUE)Formatting Python code...$(NC)"
	find units -name "*.py" -exec black {} \;
	find ops/scripts -name "*.py" -exec black {} \;
	find units -name "*.py" -exec isort {} \;
	find ops/scripts -name "*.py" -exec isort {} \;
	@echo "$(GREEN)Code formatting completed$(NC)"

security: ## Run security checks
	@echo "$(BLUE)Running security checks...$(NC)"
	find units -name "*.py" -exec bandit {} \; || true
	find ops/scripts -name "*.py" -exec bandit {} \; || true
	@echo "$(GREEN)Security checks completed$(NC)"

validate: ## Validate configuration files
	@echo "$(BLUE)Validating configuration files...$(NC)"
	docker-compose -f $(COMPOSE_FILE) config > /dev/null
	docker-compose -f $(COMPOSE_PROD_FILE) config > /dev/null
	$(PYTHON) -c "import yaml; [yaml.safe_load(open(f)) for f in ['units/lm-studio-bridge/unit.yml', 'units/unified-gateway/unit.yml']]"
	@echo "$(GREEN)Configuration validation completed$(NC)"

# =============================================================================
# MONITORING AND DEBUGGING
# =============================================================================

logs: ## Show logs from all services
	@echo "$(BLUE)Showing service logs...$(NC)"
	docker-compose -f $(COMPOSE_FILE) logs -f

logs-gateway: ## Show gateway logs only
	@echo "$(BLUE)Showing gateway logs...$(NC)"
	docker-compose -f $(COMPOSE_FILE) logs -f unified-gateway

logs-bridge: ## Show bridge logs only
	@echo "$(BLUE)Showing bridge logs...$(NC)"
	docker-compose -f $(COMPOSE_FILE) logs -f lm-studio-bridge

health: ## Check health of all services
	@echo "$(BLUE)Checking service health...$(NC)"
	@echo "Gateway Health:"
	@curl -s http://localhost:8080/health | $(PYTHON) -m json.tool 2>/dev/null || echo "Gateway not responding"
	@echo ""
	@echo "Bridge Health:"
	@curl -s http://localhost:3000/health | $(PYTHON) -m json.tool 2>/dev/null || echo "Bridge not responding"
	@echo ""
	@echo "Docker Status:"
	@docker-compose -f $(COMPOSE_FILE) ps

status: ## Show status of all services
	@echo "$(BLUE)Service Status:$(NC)"
	docker-compose -f $(COMPOSE_FILE) ps

# =============================================================================
# DEVELOPMENT UTILITIES
# =============================================================================

shell-gateway: ## Open shell in gateway container
	@echo "$(BLUE)Opening shell in gateway container...$(NC)"
	docker-compose -f $(COMPOSE_FILE) exec unified-gateway /bin/sh

shell-bridge: ## Open shell in bridge container
	@echo "$(BLUE)Opening shell in bridge container...$(NC)"
	docker-compose -f $(COMPOSE_FILE) exec lm-studio-bridge /bin/sh

mock: ## Start mock LM Studio server
	@echo "$(BLUE)Starting mock LM Studio server...$(NC)"
	cd ops/scripts && $(PYTHON) lm-studio-mock.py &
	@echo "$(GREEN)Mock server started on port 1234$(NC)"

# =============================================================================
# CLEANUP
# =============================================================================

clean: ## Clean up Docker resources
	@echo "$(BLUE)Cleaning up Docker resources...$(NC)"
	docker-compose -f $(COMPOSE_FILE) down --rmi local --volumes --remove-orphans
	docker system prune -f
	@echo "$(GREEN)Cleanup completed$(NC)"

clean-all: ## Clean up everything including images
	@echo "$(BLUE)Cleaning up all Docker resources...$(NC)"
	docker-compose -f $(COMPOSE_FILE) down --rmi all --volumes --remove-orphans
	docker-compose -f $(COMPOSE_PROD_FILE) down --rmi all --volumes --remove-orphans 2>/dev/null || true
	docker system prune -a -f
	@echo "$(GREEN)Complete cleanup finished$(NC)"

# =============================================================================
# DOCUMENTATION
# =============================================================================

docs: ## Generate documentation
	@echo "$(BLUE)Generating documentation...$(NC)"
	@echo "Documentation is already available in docs/ directory"
	@echo "$(YELLOW)Open docs/dashboard/index.html for health dashboard$(NC)"
	@echo "$(GREEN)Documentation ready$(NC)"

docs-serve: ## Serve documentation locally
	@echo "$(BLUE)Serving documentation on http://localhost:8000$(NC)"
	cd docs && $(PYTHON) -m http.server 8000

# =============================================================================
# RELEASE AND DEPLOYMENT
# =============================================================================

version: ## Show current version
	@echo "$(BLUE)Current Version:$(NC)"
	@grep -E '^version:' units/*/unit.yml | head -1 | cut -d'"' -f2 || echo "Version not found"

release: ## Create a new release (requires VERSION parameter)
	@if [ -z "$(VERSION)" ]; then \
		echo "$(RED)Error: VERSION parameter required$(NC)"; \
		echo "Usage: make release VERSION=1.0.0"; \
		exit 1; \
	fi
	@echo "$(BLUE)Creating release $(VERSION)...$(NC)"
	git tag -a v$(VERSION) -m "Release v$(VERSION)"
	git push origin v$(VERSION)
	@echo "$(GREEN)Release v$(VERSION) created$(NC)"

deploy-staging: ## Deploy to staging environment
	@echo "$(BLUE)Deploying to staging...$(NC)"
	@echo "$(YELLOW)Staging deployment not implemented yet$(NC)"

deploy-prod: ## Deploy to production environment
	@echo "$(BLUE)Deploying to production...$(NC)"
	@echo "$(YELLOW)Production deployment not implemented yet$(NC)"

# =============================================================================
# QUICK COMMANDS
# =============================================================================

dev: setup start ## Quick development setup
	@echo "$(GREEN)Development environment ready!$(NC)"

quick-test: ## Quick test run (health + basic functionality)
	@echo "$(BLUE)Running quick tests...$(NC)"
	@make health
	cd ops/scripts && $(PYTHON) inference-test.py
	@echo "$(GREEN)Quick tests completed$(NC)"

# =============================================================================
# HELP AND INFO
# =============================================================================

info: ## Show system information
	@echo "$(BLUE)System Information:$(NC)"
	@echo "Docker version: $$(docker --version)"
	@echo "Docker Compose version: $$(docker-compose --version)"
	@echo "Python version: $$($(PYTHON) --version)"
	@echo "Current directory: $$(pwd)"
	@echo "Available disk space: $$(df -h . | tail -1 | awk '{print $$4}')"

env: ## Show environment variables
	@echo "$(BLUE)Environment Variables:$(NC)"
	@echo "COMPOSE_FILE: $(COMPOSE_FILE)"
	@echo "PYTHON: $(PYTHON)"
	@echo "PIP: $(PIP)"
	@if [ -f ops/compose/.env ]; then \
		echo "Environment file exists: ops/compose/.env"; \
	else \
		echo "$(YELLOW)Environment file missing: ops/compose/.env$(NC)"; \
	fi
