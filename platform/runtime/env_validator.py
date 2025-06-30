"""
Environment Variable Validator
Validates required environment variables for platform services
"""

import os
from typing import List, Dict, Any, Optional, Union


class EnvValidationError(Exception):
    """Raised when environment validation fails"""
    pass


class EnvValidator:
    """Validates environment variables for services"""
    
    def __init__(self):
        self.required_vars: List[str] = []
        self.optional_vars: Dict[str, str] = {}
    
    def require(self, var_name: str) -> 'EnvValidator':
        """Mark an environment variable as required
        
        Args:
            var_name: Name of the environment variable
            
        Returns:
            Self for method chaining
        """
        self.required_vars.append(var_name)
        return self
    
    def optional(self, var_name: str, default_value: str) -> 'EnvValidator':
        """Mark an environment variable as optional with default
        
        Args:
            var_name: Name of the environment variable
            default_value: Default value if not set
            
        Returns:
            Self for method chaining
        """
        self.optional_vars[var_name] = default_value
        return self
    
    def validate(self) -> Dict[str, str]:
        """Validate all configured environment variables
        
        Returns:
            Dictionary of validated environment variables
            
        Raises:
            EnvValidationError: If required variables are missing
        """
        missing_vars = []
        env_vars = {}
        
        # Check required variables
        for var_name in self.required_vars:
            value = os.getenv(var_name)
            if value is None:
                missing_vars.append(var_name)
            else:
                env_vars[var_name] = value
        
        if missing_vars:
            raise EnvValidationError(
                f"Missing required environment variables: {', '.join(missing_vars)}"
            )
        
        # Set optional variables with defaults
        for var_name, default_value in self.optional_vars.items():
            env_vars[var_name] = os.getenv(var_name, default_value)
        
        return env_vars
    
    def get_int(self, var_name: str, default: Optional[int] = None) -> int:
        """Get environment variable as integer
        
        Args:
            var_name: Name of the environment variable
            default: Default value if not set or invalid
            
        Returns:
            Integer value
            
        Raises:
            EnvValidationError: If variable is required but missing/invalid
        """
        value = os.getenv(var_name)
        
        if value is None:
            if default is not None:
                return default
            raise EnvValidationError(f"Required environment variable not set: {var_name}")
        
        try:
            return int(value)
        except ValueError:
            if default is not None:
                return default
            raise EnvValidationError(f"Invalid integer value for {var_name}: {value}")
    
    def get_bool(self, var_name: str, default: Optional[bool] = None) -> bool:
        """Get environment variable as boolean
        
        Args:
            var_name: Name of the environment variable
            default: Default value if not set
            
        Returns:
            Boolean value
        """
        value = os.getenv(var_name)
        
        if value is None:
            if default is not None:
                return default
            raise EnvValidationError(f"Required environment variable not set: {var_name}")
        
        return value.lower() in ('true', '1', 'yes', 'on')
