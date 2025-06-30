"""
Service Recovery Manager for LM Studio Bridge
Handles automatic recovery from all common errors without user intervention
"""

import asyncio
import os
from typing import Dict, Any, Optional, List
from pathlib import Path
import sys

# Add platform to Python path
platform_path = Path(__file__).parent.parent.parent.parent / "platform"
sys.path.insert(0, str(platform_path))

from platform.runtime.bootstrap import get_logger
from platform.runtime.error_handler import ServiceError, NetworkError

# Import predictive maintenance
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "health-monitor"))
from predictive_maintenance import PredictiveMaintenance


class RecoveryManager:
    """Manages automatic recovery from all service errors"""

    def __init__(self, http_client=None, discovery_service=None, predictive_maintenance=None):
        """Initialize recovery manager

        Args:
            http_client: LMStudioClient instance
            discovery_service: ModelDiscovery instance
            predictive_maintenance: PredictiveMaintenance instance
        """
        self.logger = get_logger(__name__)
        self.http_client = http_client
        self.discovery_service = discovery_service
        self.predictive_maintenance = predictive_maintenance or PredictiveMaintenance()

        # Recovery state tracking
        self._recovery_attempts = 0
        self._max_recovery_attempts = 5
        self._last_recovery_time = 0
        self._recovery_cooldown = 60  # 1 minute between recovery attempts

        # Error pattern tracking
        self._error_patterns = {}
        self._recovery_strategies = {
            "connection_refused": self._recover_connection_refused,
            "timeout": self._recover_timeout,
            "service_unavailable": self._recover_service_unavailable,
            "circuit_breaker": self._recover_circuit_breaker,
            "network_error": self._recover_network_error
        }

    async def handle_error(self, error: Exception, context: str = "") -> bool:
        """Handle any error with automatic recovery

        Args:
            error: The error that occurred
            context: Context information about where the error occurred

        Returns:
            True if recovery was successful, False otherwise
        """
        current_time = asyncio.get_event_loop().time()

        # Check recovery cooldown
        if current_time - self._last_recovery_time < self._recovery_cooldown:
            self.logger.info(f"Recovery cooldown active, skipping recovery for: {error}")
            return False

        # Check max recovery attempts
        if self._recovery_attempts >= self._max_recovery_attempts:
            self.logger.error(f"Max recovery attempts ({self._max_recovery_attempts}) reached")
            return False

        self.logger.info(f"Attempting automatic recovery for error: {error} (context: {context})")

        # Record error for predictive analysis
        if self.predictive_maintenance:
            error_pattern = self._identify_error_pattern(error)
            self.predictive_maintenance.record_error(error_pattern)

        # Identify error pattern and apply appropriate recovery strategy
        error_pattern = self._identify_error_pattern(error)
        recovery_strategy = self._recovery_strategies.get(error_pattern, self._recover_generic)

        try:
            self._recovery_attempts += 1
            self._last_recovery_time = current_time

            success = await recovery_strategy(error, context)

            if success:
                self.logger.info(f"Recovery successful for {error_pattern}")
                self._recovery_attempts = 0  # Reset on success
                return True
            else:
                self.logger.warning(f"Recovery failed for {error_pattern}")
                return False

        except Exception as recovery_error:
            self.logger.error(f"Recovery attempt failed with error: {recovery_error}")
            return False

    def _identify_error_pattern(self, error: Exception) -> str:
        """Identify the error pattern to determine recovery strategy"""
        error_str = str(error).lower()

        if "connection refused" in error_str:
            return "connection_refused"
        elif "timeout" in error_str:
            return "timeout"
        elif "service unavailable" in error_str or "503" in error_str:
            return "service_unavailable"
        elif "circuit breaker" in error_str:
            return "circuit_breaker"
        elif isinstance(error, NetworkError):
            return "network_error"
        else:
            return "generic"

    async def _recover_connection_refused(self, error: Exception, context: str) -> bool:
        """Recover from connection refused errors (LM Studio not running)"""
        self.logger.info("Attempting recovery from connection refused error")

        # Wait for LM Studio to potentially start up
        await asyncio.sleep(10)

        # Try to recover HTTP client connection
        if self.http_client and hasattr(self.http_client, 'attempt_recovery'):
            return await self.http_client.attempt_recovery()

        return False

    async def _recover_timeout(self, error: Exception, context: str) -> bool:
        """Recover from timeout errors"""
        self.logger.info("Attempting recovery from timeout error")

        # Wait a bit and try to reconnect
        await asyncio.sleep(5)

        if self.http_client and hasattr(self.http_client, 'attempt_recovery'):
            return await self.http_client.attempt_recovery()

        return False

    async def _recover_service_unavailable(self, error: Exception, context: str) -> bool:
        """Recover from service unavailable errors"""
        self.logger.info("Attempting recovery from service unavailable error")

        # Wait longer for service to become available
        await asyncio.sleep(30)

        if self.http_client and await self.http_client.health_check():
            return True

        return False

    async def _recover_circuit_breaker(self, error: Exception, context: str) -> bool:
        """Recover from circuit breaker errors"""
        self.logger.info("Attempting recovery from circuit breaker error")

        # Wait for circuit breaker timeout and try recovery
        await asyncio.sleep(60)

        if self.http_client and hasattr(self.http_client, 'attempt_recovery'):
            return await self.http_client.attempt_recovery()

        return False

    async def _recover_network_error(self, error: Exception, context: str) -> bool:
        """Recover from general network errors"""
        self.logger.info("Attempting recovery from network error")

        # Progressive backoff recovery
        for wait_time in [5, 15, 30]:
            await asyncio.sleep(wait_time)

            if self.http_client and await self.http_client.health_check():
                return True

        return False

    async def _recover_generic(self, error: Exception, context: str) -> bool:
        """Generic recovery strategy for unknown errors"""
        self.logger.info(f"Attempting generic recovery for unknown error: {error}")

        # Wait and try basic health check
        await asyncio.sleep(10)

        if self.http_client and await self.http_client.health_check():
            return True

        return False

    def get_recovery_status(self) -> Dict[str, Any]:
        """Get current recovery status and metrics"""
        current_time = asyncio.get_event_loop().time()

        return {
            "recovery_attempts": self._recovery_attempts,
            "max_recovery_attempts": self._max_recovery_attempts,
            "last_recovery_time": self._last_recovery_time,
            "seconds_since_last_recovery": current_time - self._last_recovery_time,
            "recovery_cooldown_active": (current_time - self._last_recovery_time) < self._recovery_cooldown,
            "recovery_available": self._recovery_attempts < self._max_recovery_attempts
        }

    def reset_recovery_state(self):
        """Reset recovery state (for manual intervention)"""
        self.logger.info("Recovery state reset manually")
        self._recovery_attempts = 0
        self._last_recovery_time = 0
        self._error_patterns.clear()
