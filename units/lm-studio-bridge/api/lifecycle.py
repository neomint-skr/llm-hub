"""
MCP Lifecycle Handlers for LM Studio Bridge
Handles startup, ready, shutdown phases and health checks
"""

from typing import Optional
from pathlib import Path
import sys

# Add platform to Python path
platform_path = Path(__file__).parent.parent.parent.parent / "platform"
sys.path.insert(0, str(platform_path))

from platform.runtime.bootstrap import get_logger
from platform.runtime.lifecycle import LifecycleManager, HealthStatus
from platform.runtime.error_handler import ServiceError
from ..logic.http_client import LMStudioClient
from ..logic.discovery import ModelDiscovery
from ..logic.translator import MCPTranslator


class BridgeLifecycleManager:
    """Lifecycle management for LM Studio Bridge"""
    
    def __init__(self):
        self.logger = get_logger(__name__)
        self.lifecycle = LifecycleManager("lm-studio-bridge")
        
        # Service components
        self.http_client: Optional[LMStudioClient] = None
        self.discovery: Optional[ModelDiscovery] = None
        self.translator: Optional[MCPTranslator] = None
        
        # Setup lifecycle handlers
        self._setup_handlers()
    
    def _setup_handlers(self):
        """Setup lifecycle phase handlers"""
        self.lifecycle.add_startup_handler(self._startup_handler)
        self.lifecycle.add_ready_handler(self._ready_handler)
        self.lifecycle.add_shutdown_handler(self._shutdown_handler)
        
        # Setup health check providers
        self.lifecycle.add_health_provider("lm_studio", self._check_lm_studio_health)
        self.lifecycle.add_health_provider("models", self._check_models_health)
        self.lifecycle.add_health_provider("discovery", self._check_discovery_health)
    
    async def _startup_handler(self):
        """Handle startup phase"""
        self.logger.info("Starting LM Studio Bridge components")
        
        try:
            # Initialize HTTP client
            self.http_client = LMStudioClient()
            self.logger.info("HTTP client initialized")
            
            # Initialize translator
            self.translator = MCPTranslator()
            await self.translator.initialize()
            self.logger.info("Translator initialized")
            
            # Initialize discovery service
            self.discovery = ModelDiscovery()
            self.logger.info("Discovery service initialized")
            
        except Exception as e:
            self.logger.error(f"Startup failed: {e}")
            raise ServiceError(f"Failed to initialize components: {e}")
    
    async def _ready_handler(self):
        """Handle ready phase"""
        self.logger.info("Preparing LM Studio Bridge for operation")
        
        try:
            # Start model discovery
            if self.discovery:
                await self.discovery.start()
                self.logger.info("Model discovery started")
            
            # Force initial model discovery
            if self.discovery:
                model_count = await self.discovery.force_discovery()
                self.logger.info(f"Initial discovery found {model_count} models")
            
            self.logger.info("LM Studio Bridge is ready")
            
        except Exception as e:
            self.logger.error(f"Ready phase failed: {e}")
            raise ServiceError(f"Failed to prepare for operation: {e}")
    
    async def _shutdown_handler(self):
        """Handle shutdown phase"""
        self.logger.info("Shutting down LM Studio Bridge")
        
        try:
            # Stop discovery service
            if self.discovery:
                await self.discovery.stop()
                self.logger.info("Discovery service stopped")
            
            # Close translator
            if self.translator:
                await self.translator.close()
                self.logger.info("Translator closed")
            
            # Close HTTP client
            if self.http_client:
                await self.http_client.close()
                self.logger.info("HTTP client closed")
            
            self.logger.info("LM Studio Bridge shutdown complete")
            
        except Exception as e:
            self.logger.error(f"Shutdown error: {e}")
            # Continue shutdown even on errors
    
    async def _check_lm_studio_health(self) -> HealthStatus:
        """Check LM Studio connectivity health"""
        if not self.http_client:
            return HealthStatus.UNHEALTHY
        
        try:
            is_healthy = await self.http_client.health_check()
            return HealthStatus.HEALTHY if is_healthy else HealthStatus.UNHEALTHY
        except Exception:
            return HealthStatus.UNHEALTHY
    
    async def _check_models_health(self) -> HealthStatus:
        """Check if models are available"""
        if not self.discovery:
            return HealthStatus.UNKNOWN
        
        try:
            has_models = self.discovery.has_models()
            return HealthStatus.HEALTHY if has_models else HealthStatus.UNHEALTHY
        except Exception:
            return HealthStatus.UNHEALTHY
    
    async def _check_discovery_health(self) -> HealthStatus:
        """Check discovery service health"""
        if not self.discovery:
            return HealthStatus.UNKNOWN
        
        try:
            # Discovery is healthy if it's running
            return HealthStatus.HEALTHY if self.discovery.running else HealthStatus.UNHEALTHY
        except Exception:
            return HealthStatus.UNHEALTHY
    
    async def startup(self):
        """Execute startup phase"""
        await self.lifecycle.startup()
    
    async def ready(self):
        """Execute ready phase"""
        await self.lifecycle.ready()
    
    async def shutdown(self):
        """Execute shutdown phase"""
        await self.lifecycle.shutdown()
    
    async def get_health_status(self):
        """Get comprehensive health status"""
        return await self.lifecycle.get_health_status()
    
    def is_shutdown_requested(self) -> bool:
        """Check if shutdown has been requested"""
        return self.lifecycle.is_shutdown_requested()
    
    def get_components(self):
        """Get initialized components for use by server
        
        Returns:
            Dictionary of initialized components
        """
        return {
            "http_client": self.http_client,
            "discovery": self.discovery,
            "translator": self.translator,
            "lifecycle": self.lifecycle
        }
