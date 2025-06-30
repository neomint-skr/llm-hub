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
from .resource_manager import ResourceManager


class ModelDiscovery:
    """Service for discovering and tracking LM Studio models"""

    def __init__(self, poll_interval: Optional[int] = None, resource_manager: Optional[ResourceManager] = None):
        """Initialize model discovery service

        Args:
            poll_interval: Polling interval in seconds (default from env)
            resource_manager: Optional resource manager for intelligent throttling
        """
        self.poll_interval = poll_interval or int(os.getenv("POLL_INTERVAL", "30"))
        self.logger = get_logger(__name__)
        self.resource_manager = resource_manager

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
        """Main polling loop for model discovery with automatic error recovery"""
        consecutive_failures = 0
        max_consecutive_failures = 3

        while self.running:
            try:
                await self._discover_models()
                consecutive_failures = 0  # Reset on success
            except Exception as e:
                consecutive_failures += 1
                self.logger.error(f"Error during model discovery (failure {consecutive_failures}): {e}")

                # Attempt recovery after multiple failures
                if consecutive_failures >= max_consecutive_failures:
                    self.logger.warning("Multiple consecutive failures, attempting recovery")
                    if await self._attempt_recovery():
                        consecutive_failures = 0
                    else:
                        # Increase poll interval to reduce load during failures
                        extended_interval = min(self.poll_interval * 2, 300)  # Cap at 5 minutes
                        self.logger.info(f"Recovery failed, extending poll interval to {extended_interval}s")
                        await asyncio.sleep(extended_interval - self.poll_interval)

            # Wait for next poll with intelligent throttling
            try:
                poll_delay = self.poll_interval

                # Apply resource-aware throttling
                if self.resource_manager:
                    if self.resource_manager.should_throttle_operation():
                        additional_delay = await self.resource_manager.get_recommended_delay()
                        poll_delay += additional_delay
                        self.logger.debug(f"Resource throttling: extending poll interval by {additional_delay}s")

                await asyncio.sleep(poll_delay)
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

    async def _attempt_recovery(self) -> bool:
        """Attempt to recover from discovery failures

        Returns:
            True if recovery successful, False otherwise
        """
        self.logger.info("Attempting discovery service recovery")

        try:
            # Try to recover the HTTP client connection
            if self.client and hasattr(self.client, 'attempt_recovery'):
                if await self.client.attempt_recovery():
                    self.logger.info("HTTP client recovery successful")
                    return True

            # If client recovery failed, try a simple health check
            if self.client and await self.client.health_check():
                self.logger.info("Discovery recovery successful via health check")
                return True

            self.logger.warning("Discovery recovery failed")
            return False

        except Exception as e:
            self.logger.error(f"Discovery recovery attempt failed: {e}")
            return False

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
