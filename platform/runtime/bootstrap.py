"""
Platform Runtime Bootstrap
Provides JSON logging setup and common initialization
"""

import logging
import json
import sys
from typing import Optional, Dict, Any


def init_logging(
    level: str = "INFO",
    service_name: Optional[str] = None,
    include_timestamp: bool = True
) -> None:
    """Initialize JSON logging for the platform
    
    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR)
        service_name: Name of the service for log context
        include_timestamp: Whether to include timestamp in logs
    """
    
    class JSONFormatter(logging.Formatter):
        """Custom formatter for JSON log output"""
        
        def format(self, record: logging.LogRecord) -> str:
            log_entry = {
                "level": record.levelname,
                "message": record.getMessage(),
                "logger": record.name,
            }
            
            if include_timestamp:
                log_entry["timestamp"] = self.formatTime(record, "%Y-%m-%dT%H:%M:%S.%fZ")
            
            if service_name:
                log_entry["service"] = service_name
            
            if record.exc_info:
                log_entry["exception"] = self.formatException(record.exc_info)
            
            # Add extra fields from record
            for key, value in record.__dict__.items():
                if key not in ('name', 'msg', 'args', 'levelname', 'levelno', 
                              'pathname', 'filename', 'module', 'lineno', 
                              'funcName', 'created', 'msecs', 'relativeCreated',
                              'thread', 'threadName', 'processName', 'process',
                              'getMessage', 'exc_info', 'exc_text', 'stack_info'):
                    log_entry[key] = value
            
            return json.dumps(log_entry, ensure_ascii=False)
    
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, level.upper()))
    
    # Remove existing handlers
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
    
    # Add JSON handler
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(JSONFormatter())
    root_logger.addHandler(handler)


def get_logger(name: str) -> logging.Logger:
    """Get a logger instance
    
    Args:
        name: Logger name (typically __name__)
        
    Returns:
        Configured logger instance
    """
    return logging.getLogger(name)


def log_startup_info(service_name: str, version: str = "1.0.0") -> None:
    """Log service startup information
    
    Args:
        service_name: Name of the starting service
        version: Service version
    """
    logger = get_logger(__name__)
    logger.info(
        "Service starting",
        extra={
            "service": service_name,
            "version": version,
            "event": "startup"
        }
    )
