"""
Logging Utilities
Provides logging functionality for the application following SOLID principles.
"""

import logging
from pathlib import Path
from datetime import datetime


class LoggerSetup:
    """
    Sets up application logging with file and console handlers.

    This class follows the Single Responsibility Principle by handling
    only the configuration of logging for the application.
    """

    _instance: "LoggerSetup | None" = None
    _loggers: dict[str, logging.Logger] = {}

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, log_dir: str = "./logs", log_level: int = logging.INFO):
        if hasattr(self, "_initialized") and self._initialized:
            return
        self.log_dir = Path(log_dir)
        self.log_level = log_level
        self._initialized = True

    def setup_logging(self):
        """Initialize logging with file and console handlers."""
        self.log_dir.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = self.log_dir / f"predictor_{timestamp}.log"

        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )

        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        file_handler.setLevel(self.log_level)
        file_handler.setFormatter(formatter)

        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.WARNING)
        console_handler.setFormatter(formatter)

        root_logger = logging.getLogger()
        root_logger.setLevel(self.log_level)
        root_logger.addHandler(file_handler)
        root_logger.addHandler(console_handler)


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance with the given name.

    Args:
        name: Logger name (usually __name__ or class name)

    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    if not logger.handlers:
        setup = LoggerSetup()
        setup.setup_logging()
    return logger
