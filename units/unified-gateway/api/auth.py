"""
Authentication Layer
Bearer token validation with environment-based API keys
"""

import os
import time
import logging
from typing import Dict, Optional
from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

logger = logging.getLogger(__name__)

# Security scheme
security = HTTPBearer()

# Rate limiting storage (in-memory)
rate_limit_storage: Dict[str, list] = {}

class AuthManager:
    """Authentication and rate limiting manager"""
    
    def __init__(self):
        self.auth_enabled = os.getenv("AUTH_ENABLED", "true").lower() == "true"
        self.api_key = os.getenv("API_KEY", "changeme")
        self.rate_limit = int(os.getenv("RATE_LIMIT_PER_MINUTE", "60"))
        
    def verify_token(self, credentials: HTTPAuthorizationCredentials = Depends(security)) -> bool:
        """Verify bearer token"""
        if not self.auth_enabled:
            return True
            
        if credentials.credentials != self.api_key:
            logger.warning(f"Invalid token attempt")
            raise HTTPException(status_code=401, detail="Invalid authentication token")
            
        # Check rate limit
        if not self._check_rate_limit(credentials.credentials):
            logger.warning(f"Rate limit exceeded for token")
            raise HTTPException(status_code=429, detail="Rate limit exceeded")
            
        return True
    
    def _check_rate_limit(self, token: str) -> bool:
        """Check rate limit for token"""
        if self.rate_limit <= 0:
            return True
            
        current_time = time.time()
        minute_ago = current_time - 60
        
        # Get or create token history
        if token not in rate_limit_storage:
            rate_limit_storage[token] = []
            
        token_history = rate_limit_storage[token]
        
        # Remove old entries
        rate_limit_storage[token] = [
            timestamp for timestamp in token_history 
            if timestamp > minute_ago
        ]
        
        # Check if under limit
        if len(rate_limit_storage[token]) >= self.rate_limit:
            return False
            
        # Add current request
        rate_limit_storage[token].append(current_time)
        return True
    
    def get_auth_status(self) -> Dict[str, any]:
        """Get authentication status"""
        return {
            "auth_enabled": self.auth_enabled,
            "rate_limit_per_minute": self.rate_limit,
            "active_tokens": len(rate_limit_storage)
        }

# Global auth manager instance
auth_manager = AuthManager()

def get_auth_dependency():
    """Get authentication dependency for FastAPI"""
    return Depends(auth_manager.verify_token)

def optional_auth_dependency():
    """Optional authentication dependency"""
    if auth_manager.auth_enabled:
        return Depends(auth_manager.verify_token)
    return lambda: True
