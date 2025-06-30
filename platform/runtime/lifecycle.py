"""
MCP Lifecycle Management
Handles MCP-standard lifecycle phases and graceful shutdown
"""

import signal
import asyncio
import logging
from typing import Dict, List, Callable, Optional, Any
from enum import Enum


class LifecyclePhase(Enum):
    """MCP standard lifecycle phases"""
    STARTUP = "startup"
    READY = "ready"
    SHUTDOWN = "shutdown"


class HealthStatus(Enum):
    """Health check status values"""
    HEALTHY = "healthy"
    UNHEALTHY = "unhealthy"
    UNKNOWN = "unknown"


class LifecycleManager:
    """Manages MCP lifecycle phases and health checks"""
    
    def __init__(self, service_name: str):
        self.service_name = service_name
        self.current_phase = LifecyclePhase.STARTUP
        self.logger = logging.getLogger(__name__)
        
        # Lifecycle handlers
        self._startup_handlers: List[Callable] = []
        self._ready_handlers: List[Callable] = []
        self._shutdown_handlers: List[Callable] = []
        
        # Health check providers
        self._health_providers: Dict[str, Callable] = {}
        
        # Shutdown flag
        self._shutdown_requested = False
        
        # Setup signal handlers
        self._setup_signal_handlers()
    
    def _setup_signal_handlers(self) -> None:
        """Setup signal handlers for graceful shutdown"""
        def signal_handler(signum, frame):
            self.logger.info(f"Received signal {signum}, initiating shutdown")
            self._shutdown_requested = True
        
        signal.signal(signal.SIGTERM, signal_handler)
        signal.signal(signal.SIGINT, signal_handler)
    
    def add_startup_handler(self, handler: Callable) -> None:
        """Add a startup phase handler
        
        Args:
            handler: Async or sync function to call during startup
        """
        self._startup_handlers.append(handler)
    
    def add_ready_handler(self, handler: Callable) -> None:
        """Add a ready phase handler
        
        Args:
            handler: Async or sync function to call when ready
        """
        self._ready_handlers.append(handler)
    
    def add_shutdown_handler(self, handler: Callable) -> None:
        """Add a shutdown phase handler
        
        Args:
            handler: Async or sync function to call during shutdown
        """
        self._shutdown_handlers.append(handler)
    
    def add_health_provider(self, name: str, provider: Callable) -> None:
        """Add a health check provider
        
        Args:
            name: Name of the health check
            provider: Function that returns health status
        """
        self._health_providers[name] = provider
    
    async def startup(self) -> None:
        """Execute startup phase"""
        self.logger.info("Starting startup phase")
        self.current_phase = LifecyclePhase.STARTUP
        
        for handler in self._startup_handlers:
            try:
                if asyncio.iscoroutinefunction(handler):
                    await handler()
                else:
                    handler()
            except Exception as e:
                self.logger.error(f"Startup handler failed: {e}")
                raise
        
        self.logger.info("Startup phase completed")
    
    async def ready(self) -> None:
        """Execute ready phase"""
        self.logger.info("Entering ready phase")
        self.current_phase = LifecyclePhase.READY
        
        for handler in self._ready_handlers:
            try:
                if asyncio.iscoroutinefunction(handler):
                    await handler()
                else:
                    handler()
            except Exception as e:
                self.logger.error(f"Ready handler failed: {e}")
                raise
        
        self.logger.info("Service is ready")
    
    async def shutdown(self) -> None:
        """Execute shutdown phase"""
        self.logger.info("Starting shutdown phase")
        self.current_phase = LifecyclePhase.SHUTDOWN
        
        for handler in self._shutdown_handlers:
            try:
                if asyncio.iscoroutinefunction(handler):
                    await handler()
                else:
                    handler()
            except Exception as e:
                self.logger.error(f"Shutdown handler failed: {e}")
                # Continue with other handlers
        
        self.logger.info("Shutdown phase completed")
    
    def is_shutdown_requested(self) -> bool:
        """Check if shutdown has been requested"""
        return self._shutdown_requested
    
    async def get_health_status(self) -> Dict[str, Any]:
        """Get aggregated health status from all providers
        
        Returns:
            Health status dictionary
        """
        overall_status = HealthStatus.HEALTHY
        checks = {}
        
        for name, provider in self._health_providers.items():
            try:
                if asyncio.iscoroutinefunction(provider):
                    status = await provider()
                else:
                    status = provider()
                
                checks[name] = {
                    "status": status.value if isinstance(status, HealthStatus) else str(status),
                    "timestamp": asyncio.get_event_loop().time()
                }
                
                # If any check is unhealthy, overall status is unhealthy
                if status == HealthStatus.UNHEALTHY:
                    overall_status = HealthStatus.UNHEALTHY
                    
            except Exception as e:
                self.logger.error(f"Health check {name} failed: {e}")
                checks[name] = {
                    "status": HealthStatus.UNHEALTHY.value,
                    "error": str(e),
                    "timestamp": asyncio.get_event_loop().time()
                }
                overall_status = HealthStatus.UNHEALTHY
        
        return {
            "service": self.service_name,
            "status": overall_status.value,
            "phase": self.current_phase.value,
            "checks": checks
        }
