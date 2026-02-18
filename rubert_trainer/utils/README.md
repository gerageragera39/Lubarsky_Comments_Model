# Utils Module

## Overview

The `utils` module provides shared utility functions and helper classes used across the application. It contains infrastructure code for logging that follows the Single Responsibility Principle.

## Architecture

This module follows the **Single Responsibility Principle** from SOLID design patterns. Each utility class handles a specific cross-cutting concern, ensuring reusability and separation of concerns.

## Files

### `__init__.py`

Package initialization file that exports utility classes and functions for external module access.

### `logging_utils.py`

**Purpose:** Provides centralized logging configuration for the entire application.

**Key Classes:**

#### `LoggerSetup`

A singleton-like class that configures application-wide logging with both file and console output.

**Purpose:** Initializes logging infrastructure with appropriate formatters, handlers, and log levels.

**Attributes:**

| Attribute | Type | Default | Description |
|-----------|------|---------|-------------|
| `log_dir` | `Path` | `"./logs"` | Directory for log files |
| `log_level` | `int` | `logging.INFO` | Logging verbosity level |
| `logger` | `Logger` | `None` | Configured logger instance |

**Methods:**

| Method | Returns | Description |
|--------|---------|-------------|
| `setup_logging()` | `logging.Logger` | Initializes and returns configured logger |

**Log Configuration:**

| Property | Value |
|----------|-------|
| Logger Name | `rubert_trainer` |
| Log Level | `INFO` (configurable) |
| Log Format | `%(asctime)s - %(name)s - %(levelname)s - %(message)s` |
| Log Filename | `rubert_trainer_YYYYMMDD_HHMMSS.log` |

**Handlers:**

| Handler | Level | Purpose |
|---------|-------|---------|
| `StreamHandler` | INFO | Console output for real-time debugging |
| `FileHandler` | INFO | Persistent log file for post-mortem analysis |

**Features:**

1. **Automatic Directory Creation:** Creates log directory if it doesn't exist
2. **Duplicate Handler Prevention:** Checks for existing handlers before adding new ones
3. **Timestamped Log Files:** Each session gets a unique log file with timestamp
4. **Dual Output:** Logs appear both in console and file simultaneously

**Usage Example:**
```python
from utils.logging_utils import LoggerSetup, get_logger

# Initialize logging (typically in application entry point)
logger_setup = LoggerSetup(log_dir="./logs", log_level=logging.INFO)
logger_setup.setup_logging()

# Get logger in any module
logger = get_logger("MyClass")
logger.info("Application started")
logger.debug("Debug information")
logger.warning("Warning message")
logger.error("Error occurred")
```

**Log Output Example:**
```
2025-02-16 14:30:45,123 - rubert_trainer.TrainingService - INFO - Starting training process
2025-02-16 14:30:46,456 - rubert_trainer.TrainingService - DEBUG - Loading dataset from: data.csv
2025-02-16 14:30:47,789 - rubert_trainer.TrainingService - INFO - Dataset loaded with 10000 rows
2025-02-16 14:35:22,012 - rubert_trainer.TrainingService - ERROR - File not found: missing.csv
```

#### `get_logger()`

A convenience function for obtaining named loggers within modules.

**Parameters:**
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `name` | `str` | `None` | Optional name for logger (typically class name) |

**Returns:** `logging.Logger` - Configured logger instance

**Naming Convention:**
- Without name: `rubert_trainer`
- With name: `rubert_trainer.{name}`

**Usage:**
```python
# In a class
class TrainingService:
    def __init__(self):
        self.logger = get_logger(self.__class__.__name__)
        # Logger name: rubert_trainer.TrainingService

# In a module
logger = get_logger("data_loader")
# Logger name: rubert_trainer.data_loader
```

## Dependencies

- **logging:** Python standard library logging module
- **datetime:** Timestamp generation for log filenames
- **pathlib:** Cross-platform path manipulation

## Design Patterns

- **Singleton Pattern (implicit):** `LoggerSetup` ensures single logger configuration per application instance
- **Factory Pattern:** `get_logger()` function acts as a logger factory
- **Template Method Pattern:** Logging format is templated for consistency

## Log File Structure

Log files are stored in the `./logs` directory (configurable) with the following naming convention:

```
logs/
├── rubert_trainer_20250216_143045.log
├── rubert_trainer_20250216_151230.log
└── rubert_trainer_20250217_091500.log
```

Each log file corresponds to a single application session.

## Integration Points

- **Main Entry Point (`__main__.py`):** Initializes logging on application startup
- **All Modules:** Use `get_logger()` for consistent logging across the application
- **Training Service:** Extensive logging for training progress and debugging

## Best Practices

1. **Use Appropriate Log Levels:**
   - `DEBUG`: Detailed technical information for debugging
   - `INFO`: General operational messages
   - `WARNING`: Unexpected but handled situations
   - `ERROR`: Error conditions that may require attention
   - `CRITICAL`: Severe errors requiring immediate action

2. **Include Context in Messages:**
   ```python
   # Good
   logger.info(f"Dataset loaded with {len(df)} rows from {csv_path}")
   
   # Bad
   logger.info("Dataset loaded")
   ```

3. **Log Exceptions with Stack Trace:**
   ```python
   try:
       # ... code ...
   except Exception as e:
       logger.error(f"Operation failed: {e}", exc_info=True)
   ```

---

## TODO: Potential Improvements

- [ ] **TODO:** The `setup_logging()` method returns the logger but stores it in `self.logger` instance variable. Since `LoggerSetup` is typically instantiated once and discarded, consider making this a static method or module-level function for simplicity.

- [ ] **TODO:** Log files are never automatically cleaned up. Consider implementing log rotation using `logging.handlers.RotatingFileHandler` or `TimedRotatingFileHandler` to prevent disk space exhaustion:
  ```python
  from logging.handlers import RotatingFileHandler
  handler = RotatingFileHandler(filename, maxBytes=10*1024*1024, backupCount=5)
  ```

- [ ] **TODO:** The log level is fixed at initialization time. Consider adding support for runtime log level configuration (e.g., through environment variable `LOG_LEVEL` or command-line argument) for debugging production issues.

- [ ] **TODO:** No structured logging (JSON format) is available. For better log analysis and integration with log aggregation systems (ELK, Splunk), consider adding an optional JSON formatter.

- [ ] **TODO:** The logger name hierarchy (`rubert_trainer.module.class`) could be leveraged for selective log level configuration per module, but no API is provided for this. Consider adding `set_level_for_module(module_name, level)` function.
