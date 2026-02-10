"""
Logging Utilities
Provides logging functionality for the application following SOLID principles.
"""

import logging
import os
from datetime import datetime
from pathlib import Path


class LoggerSetup:
    """
    Sets up application logging with file and console handlers.
    
    This class follows the Single Responsibility Principle by handling
    only the configuration of logging for the application.
    """
    
    def __init__(self, log_dir: str = "./logs", log_level: int = logging.INFO):
        self.log_dir = Path(log_dir)
        self.log_level = log_level
        self.logger = None
        
    def setup_logging(self):
        """Initialize logging with file and console handlers."""
        # Create log directory if it doesn't exist
        self.log_dir.mkdir(parents=True, exist_ok=True)
        
        # Create logger
        self.logger = logging.getLogger('rubert_trainer')
        self.logger.setLevel(self.log_level)
        
        # Prevent adding handlers multiple times
        if self.logger.handlers:
            return self.logger
            
        # Create formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(self.log_level)
        console_handler.setFormatter(formatter)
        
        # File handler
        log_filename = self.log_dir / f"rubert_trainer_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        file_handler = logging.FileHandler(log_filename)
        file_handler.setLevel(self.log_level)
        file_handler.setFormatter(formatter)
        
        # Add handlers to logger
        self.logger.addHandler(console_handler)
        self.logger.addHandler(file_handler)
        
        return self.logger


def get_logger(name: str = None):
    """
    Get a logger instance.
    
    :param name: Name of the logger (optional)
    :return: Logger instance
    """
    logger_name = f"rubert_trainer.{name}" if name else "rubert_trainer"
    return logging.getLogger(logger_name)