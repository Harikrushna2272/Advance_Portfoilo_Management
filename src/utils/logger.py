# Logging utilities for StockAI
import logging
import os
from datetime import datetime
from typing import Optional
from src.config.settings import get_settings


def setup_logger(
    name: str = "stockai",
    log_file: Optional[str] = None,
    log_level: str = "INFO"
) -> logging.Logger:
    """
    Set up logger with file and console handlers.
    
    Args:
        name: Logger name
        log_file: Log file path (optional)
        log_level: Logging level
        
    Returns:
        Configured logger instance
    """
    settings = get_settings()
    
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, log_level.upper()))
    
    # Clear existing handlers
    logger.handlers.clear()
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(getattr(logging, log_level.upper()))
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # File handler
    if log_file:
        # Create logs directory if it doesn't exist
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
        
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(getattr(logging, log_level.upper()))
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger


def get_logger(name: str = "stockai") -> logging.Logger:
    """Get existing logger or create new one."""
    return logging.getLogger(name)


# Create default logger
default_logger = setup_logger()
