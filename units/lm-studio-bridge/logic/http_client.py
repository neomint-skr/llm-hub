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
    """Async HTTP client for LM Studio API"""
    
    def __init__(self, base_url: Optional[str] = None, timeout: int = 30, max_retries: int = 3):
        """Initialize LM Studio HTTP client
        
        Args:
            base_url: Base URL for LM Studio API
            timeout: Request timeout in seconds
            max_retries: Maximum number of retries for failed requests
        """
        self.base_url = base_url or os.getenv("LM_STUDIO_URL", "http://localhost:1234")
        self.timeout = timeout
        self.max_retries = max_retries
        self.logger = get_logger(__name__)
        
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
    
    async def _make_request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """Make HTTP request with retry logic
        
        Args:
            method: HTTP method (GET, POST, etc.)
            endpoint: API endpoint
            **kwargs: Additional request parameters
            
        Returns:
            Response data as dictionary
            
        Raises:
            NetworkError: If request fails after all retries
        """
        last_error = None
        
        for attempt in range(self.max_retries + 1):
            try:
                response = await self.client.request(method, endpoint, **kwargs)
                response.raise_for_status()
                
                # Try to parse JSON response
                try:
                    return response.json()
                except ValueError:
                    # Return text if not JSON
                    return {"text": response.text}
                    
            except httpx.HTTPStatusError as e:
                last_error = e
                self.logger.warning(f"HTTP error {e.response.status_code} on attempt {attempt + 1}")
                
                # Don't retry on client errors (4xx)
                if 400 <= e.response.status_code < 500:
                    break
                    
            except (httpx.RequestError, httpx.TimeoutException) as e:
                last_error = e
                self.logger.warning(f"Request error on attempt {attempt + 1}: {e}")
            
            # Exponential backoff for retries
            if attempt < self.max_retries:
                wait_time = 2 ** attempt
                self.logger.info(f"Retrying in {wait_time} seconds...")
                await asyncio.sleep(wait_time)
        
        # All retries failed
        raise NetworkError(
            f"Request to {endpoint} failed after {self.max_retries + 1} attempts",
            details={"last_error": str(last_error)}
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
