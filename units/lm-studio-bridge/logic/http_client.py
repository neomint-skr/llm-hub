"""
HTTP Client for LM Studio API
Async HTTP client with connection pooling and retry logic
"""

import asyncio
import os
from typing import Dict, Any, Optional, List
import httpx
from pathlib import Path
import sys

# Add platform to Python path
platform_path = Path(__file__).parent.parent.parent.parent / "platform"
sys.path.insert(0, str(platform_path))

from platform.runtime.bootstrap import get_logger
from platform.runtime.error_handler import NetworkError


class LMStudioClient:
    """Async HTTP client for LM Studio API with complete error recovery"""

    def __init__(self, base_url: Optional[str] = None, timeout: int = 30, max_retries: int = 3, resource_manager=None):
        """Initialize LM Studio HTTP client

        Args:
            base_url: Base URL for LM Studio API
            timeout: Request timeout in seconds
            max_retries: Maximum number of retries for failed requests
            resource_manager: Optional resource manager for intelligent throttling
        """
        self.base_url = base_url or os.getenv("LM_STUDIO_URL", "http://localhost:1234")
        self.timeout = timeout
        self.max_retries = max_retries
        self.logger = get_logger(__name__)
        self.resource_manager = resource_manager

        # Circuit breaker state
        self._circuit_breaker_failures = 0
        self._circuit_breaker_last_failure = 0
        self._circuit_breaker_threshold = 5
        self._circuit_breaker_timeout = 60
        self._is_circuit_open = False

        # Connection state tracking
        self._connection_healthy = True
        self._last_successful_request = asyncio.get_event_loop().time()

        # HTTP client with connection pooling
        self.client = httpx.AsyncClient(
            base_url=self.base_url,
            timeout=httpx.Timeout(timeout),
            limits=httpx.Limits(max_keepalive_connections=5, max_connections=10)
        )

    async def __aenter__(self):
        """Async context manager entry"""
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        await self.close()

    async def close(self):
        """Close the HTTP client"""
        await self.client.aclose()

    def _check_circuit_breaker(self) -> bool:
        """Check if circuit breaker allows requests"""
        current_time = asyncio.get_event_loop().time()

        # Reset circuit breaker after timeout
        if self._is_circuit_open and (current_time - self._circuit_breaker_last_failure) > self._circuit_breaker_timeout:
            self.logger.info("Circuit breaker timeout expired, attempting to close circuit")
            self._is_circuit_open = False
            self._circuit_breaker_failures = 0

        return not self._is_circuit_open

    def _record_success(self):
        """Record successful request"""
        self._connection_healthy = True
        self._last_successful_request = asyncio.get_event_loop().time()
        self._circuit_breaker_failures = 0
        if self._is_circuit_open:
            self.logger.info("Circuit breaker closed after successful request")
            self._is_circuit_open = False

    def _record_failure(self):
        """Record failed request and update circuit breaker"""
        self._connection_healthy = False
        self._circuit_breaker_failures += 1
        self._circuit_breaker_last_failure = asyncio.get_event_loop().time()

        if self._circuit_breaker_failures >= self._circuit_breaker_threshold:
            self._is_circuit_open = True
            self.logger.warning(f"Circuit breaker opened after {self._circuit_breaker_failures} failures")

    async def _make_request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """Make HTTP request with complete error recovery

        Args:
            method: HTTP method (GET, POST, etc.)
            endpoint: API endpoint
            **kwargs: Additional request parameters

        Returns:
            Response data as dictionary

        Raises:
            NetworkError: If request fails after all retries and circuit breaker
        """
        # Check circuit breaker
        if not self._check_circuit_breaker():
            raise NetworkError(
                f"Circuit breaker is open for {endpoint}",
                details={"circuit_breaker_failures": self._circuit_breaker_failures}
            )

        last_error = None

        for attempt in range(self.max_retries + 1):
            try:
                response = await self.client.request(method, endpoint, **kwargs)
                response.raise_for_status()

                # Success - record it and reset circuit breaker
                self._record_success()

                # Try to parse JSON response
                try:
                    return response.json()
                except ValueError:
                    # Return text if not JSON
                    return {"text": response.text}

            except httpx.HTTPStatusError as e:
                last_error = e
                self.logger.warning(f"HTTP error {e.response.status_code} on attempt {attempt + 1}")

                # Don't retry on client errors (4xx) except 429 (rate limit)
                if 400 <= e.response.status_code < 500 and e.response.status_code != 429:
                    self._record_failure()
                    break

            except (httpx.RequestError, httpx.TimeoutException) as e:
                last_error = e
                self.logger.warning(f"Request error on attempt {attempt + 1}: {e}")

                # Check if this is a connection error that might indicate LM Studio is down
                if "Connection refused" in str(e) or "timeout" in str(e).lower():
                    self.logger.info("LM Studio appears to be down, will attempt automatic recovery")

            # Record failure for circuit breaker
            self._record_failure()

            # Exponential backoff for retries with resource-aware delays
            if attempt < self.max_retries:
                wait_time = min(2 ** attempt, 30)  # Cap at 30 seconds

                # Apply additional delay if system is under resource pressure
                if self.resource_manager and self.resource_manager.should_throttle_operation():
                    additional_delay = await self.resource_manager.get_recommended_delay()
                    wait_time += additional_delay
                    self.logger.info(f"Resource throttling: adding {additional_delay}s delay")

                self.logger.info(f"Retrying in {wait_time} seconds...")
                await asyncio.sleep(wait_time)

        # All retries failed
        raise NetworkError(
            f"Request to {endpoint} failed after {self.max_retries + 1} attempts",
            details={"last_error": str(last_error), "circuit_breaker_open": self._is_circuit_open}
        )

    async def get_models(self) -> List[Dict[str, Any]]:
        """Get list of available models from LM Studio

        Returns:
            List of model dictionaries
        """
        self.logger.info("Fetching models from LM Studio")

        try:
            response = await self._make_request("GET", "/v1/models")
            models = response.get("data", [])

            self.logger.info(f"Found {len(models)} models")
            return models

        except NetworkError as e:
            self.logger.error(f"Failed to fetch models: {e}")
            raise

    async def create_completion(
        self,
        prompt: str,
        model: str,
        temperature: float = 0.7,
        max_tokens: int = 1000,
        **kwargs
    ) -> Dict[str, Any]:
        """Create text completion using LM Studio

        Args:
            prompt: Input prompt
            model: Model identifier
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate
            **kwargs: Additional completion parameters

        Returns:
            Completion response
        """
        self.logger.info(f"Creating completion with model {model}")

        payload = {
            "model": model,
            "prompt": prompt,
            "temperature": temperature,
            "max_tokens": max_tokens,
            **kwargs
        }

        try:
            response = await self._make_request("POST", "/v1/completions", json=payload)

            self.logger.info("Completion created successfully")
            return response

        except NetworkError as e:
            self.logger.error(f"Failed to create completion: {e}")
            raise

    async def health_check(self) -> bool:
        """Check if LM Studio is healthy and reachable

        Returns:
            True if healthy, False otherwise
        """
        try:
            await self._make_request("GET", "/v1/models")
            return True
        except NetworkError:
            return False

    async def attempt_recovery(self) -> bool:
        """Attempt to recover from connection failures

        Returns:
            True if recovery successful, False otherwise
        """
        self.logger.info("Attempting automatic recovery from connection failure")

        # Reset circuit breaker to allow recovery attempts
        self._is_circuit_open = False
        self._circuit_breaker_failures = 0

        # Try to reconnect with a simple health check
        try:
            # Close and recreate HTTP client to clear any connection issues
            await self.client.aclose()
            self.client = httpx.AsyncClient(
                base_url=self.base_url,
                timeout=httpx.Timeout(self.timeout),
                limits=httpx.Limits(max_keepalive_connections=5, max_connections=10)
            )

            # Test connection
            if await self.health_check():
                self.logger.info("Automatic recovery successful")
                return True
            else:
                self.logger.warning("Recovery attempt failed - LM Studio still not responding")
                return False

        except Exception as e:
            self.logger.error(f"Recovery attempt failed: {e}")
            return False

    def get_connection_status(self) -> Dict[str, Any]:
        """Get current connection status and metrics

        Returns:
            Dictionary with connection status information
        """
        current_time = asyncio.get_event_loop().time()

        return {
            "healthy": self._connection_healthy,
            "circuit_breaker_open": self._is_circuit_open,
            "circuit_breaker_failures": self._circuit_breaker_failures,
            "last_successful_request": self._last_successful_request,
            "seconds_since_last_success": current_time - self._last_successful_request,
            "base_url": self.base_url
        }
