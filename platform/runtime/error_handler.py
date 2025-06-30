"""
Common Error Handler Classes
Provides base error classes for platform services
"""

from typing import Optional, Dict, Any


class PlatformError(Exception):
    """Base exception for all platform errors"""
    
    def __init__(
        self, 
        message: str, 
        error_code: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(message)
        self.message = message
        self.error_code = error_code or self.__class__.__name__
        self.details = details or {}
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert error to dictionary for JSON serialization"""
        return {
            "error": self.error_code,
            "message": self.message,
            "details": self.details
        }


class ConfigurationError(PlatformError):
    """Raised when configuration is invalid"""
    pass


class ServiceError(PlatformError):
    """Raised when a service operation fails"""
    pass


class ValidationError(PlatformError):
    """Raised when validation fails"""
    pass


class NetworkError(PlatformError):
    """Raised when network operations fail"""
    pass


class ContractError(PlatformError):
    """Raised when contract operations fail"""
    pass


def handle_error(error: Exception, logger=None) -> Dict[str, Any]:
    """Handle and format errors for consistent response
    
    Args:
        error: The exception to handle
        logger: Optional logger for error logging
        
    Returns:
        Error dictionary for response
    """
    if isinstance(error, PlatformError):
        error_dict = error.to_dict()
    else:
        error_dict = {
            "error": "UnknownError",
            "message": str(error),
            "details": {}
        }
    
    if logger:
        logger.error(
            "Error occurred",
            extra={
                "error_code": error_dict["error"],
                "error_message": error_dict["message"],
                "error_details": error_dict["details"]
            }
        )
    
    return error_dict


class ErrorContext:
    """Context manager for error handling"""
    
    def __init__(self, operation: str, logger=None):
        self.operation = operation
        self.logger = logger
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            if self.logger:
                self.logger.error(
                    f"Error in {self.operation}",
                    extra={
                        "operation": self.operation,
                        "exception_type": exc_type.__name__,
                        "exception_message": str(exc_val)
                    }
                )
        return False  # Don't suppress exceptions
