"""
Model Discovery Service
Polls LM Studio for model changes and maintains in-memory registry
"""

import asyncio
import os
from typing import Dict, List, Set, Optional
from pathlib import Path
import sys

# Add platform to Python path
platform_path = Path(__file__).parent.parent.parent.parent / "platform"
sys.path.insert(0, str(platform_path))

from platform.runtime.bootstrap import get_logger
from platform.runtime.error_handler import ServiceError
from .http_client import LMStudioClient


class ModelDiscovery:
    """Service for discovering and tracking LM Studio models"""
    
    def __init__(self, poll_interval: Optional[int] = None):
        """Initialize model discovery service
        
        Args:
            poll_interval: Polling interval in seconds (default from env)
        """
        self.poll_interval = poll_interval or int(os.getenv("POLL_INTERVAL", "30"))
        self.logger = get_logger(__name__)
        
        # In-memory model registry
        self.models: Dict[str, Dict] = {}
        self.model_ids: Set[str] = set()
        
        # Discovery state
        self.running = False
        self.task: Optional[asyncio.Task] = None
        self.client: Optional[LMStudioClient] = None
    
    async def start(self):
        """Start the discovery service"""
        if self.running:
            self.logger.warning("Discovery service already running")
            return
        
        self.logger.info(f"Starting model discovery with {self.poll_interval}s interval")
        self.running = True
        
        # Initialize HTTP client
        self.client = LMStudioClient()
        
        # Start polling task
        self.task = asyncio.create_task(self._polling_loop())
    
    async def stop(self):
        """Stop the discovery service"""
        if not self.running:
            return
        
        self.logger.info("Stopping model discovery")
        self.running = False
        
        # Cancel polling task
        if self.task:
            self.task.cancel()
            try:
                await self.task
            except asyncio.CancelledError:
                pass
        
        # Close HTTP client
        if self.client:
            await self.client.close()
        
        self.logger.info("Model discovery stopped")
    
    async def _polling_loop(self):
        """Main polling loop for model discovery"""
        while self.running:
            try:
                await self._discover_models()
            except Exception as e:
                self.logger.error(f"Error during model discovery: {e}")
                # Continue polling even on errors
            
            # Wait for next poll
            try:
                await asyncio.sleep(self.poll_interval)
            except asyncio.CancelledError:
                break
    
    async def _discover_models(self):
        """Discover models from LM Studio"""
        if not self.client:
            raise ServiceError("HTTP client not initialized")
        
        try:
            # Fetch current models
            models_data = await self.client.get_models()
            current_model_ids = set()
            
            # Process each model
            for model_data in models_data:
                model_id = model_data.get("id")
                if not model_id:
                    continue
                
                current_model_ids.add(model_id)
                
                # Check if this is a new model
                if model_id not in self.model_ids:
                    self._handle_model_added(model_id, model_data)
                else:
                    # Update existing model data
                    self.models[model_id] = model_data
            
            # Check for removed models
            removed_models = self.model_ids - current_model_ids
            for model_id in removed_models:
                self._handle_model_removed(model_id)
            
            # Update registry
            self.model_ids = current_model_ids
            
        except Exception as e:
            self.logger.error(f"Failed to discover models: {e}")
            raise ServiceError(f"Model discovery failed: {e}")
    
    def _handle_model_added(self, model_id: str, model_data: Dict):
        """Handle new model discovery"""
        self.logger.info(f"New model discovered: {model_id}")
        self.models[model_id] = model_data
        
        # Log model details
        model_name = model_data.get("object", "unknown")
        self.logger.info(f"Model details: id={model_id}, type={model_name}")
    
    def _handle_model_removed(self, model_id: str):
        """Handle model removal"""
        self.logger.info(f"Model removed: {model_id}")
        
        # Remove from registry
        if model_id in self.models:
            del self.models[model_id]
    
    def get_models(self) -> List[Dict]:
        """Get current list of discovered models
        
        Returns:
            List of model dictionaries
        """
        return list(self.models.values())
    
    def get_model(self, model_id: str) -> Optional[Dict]:
        """Get specific model by ID
        
        Args:
            model_id: Model identifier
            
        Returns:
            Model data or None if not found
        """
        return self.models.get(model_id)
    
    def has_models(self) -> bool:
        """Check if any models are available
        
        Returns:
            True if models are available, False otherwise
        """
        return len(self.models) > 0
    
    async def force_discovery(self):
        """Force immediate model discovery
        
        Returns:
            Number of models discovered
        """
        self.logger.info("Forcing model discovery")
        
        if not self.client:
            self.client = LMStudioClient()
        
        await self._discover_models()
        return len(self.models)
