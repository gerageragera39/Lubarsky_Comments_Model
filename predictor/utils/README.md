# Utils Module

## Overview

The `utils` module provides shared utility functions and helper classes used across the application. It contains infrastructure code for logging and video URL handling that follows the Single Responsibility Principle.

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

| Attribute | Type | Description |
|-----------|------|-------------|
| `log_dir` | Path | Directory for log files |
| `log_level` | int | Logging level (default: INFO) |
| `_instance` | LoggerSetup | Singleton instance |

**Methods:**

| Method | Description |
|--------|-------------|
| `__new__` | Singleton pattern implementation |
| `__init__` | Initialize logging configuration |
| `setup_logging` | Create log directory, handlers, and formatters |

**Log Format:**
```
%(asctime)s - %(name)s - %(levelname)s - %(message)s
```

Example: `2024-01-15 10:30:45 - PredictionService - INFO - Starting prediction for video: abc123`

#### `get_logger`

Factory function for obtaining logger instances.

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `name` | str | Logger name (usually `__name__`) |

**Returns:** Configured `logging.Logger` instance

### `video_utils.py`

**Purpose:** Provides utility functions for working with YouTube video URLs.

**Functions:**

#### `extract_video_id`

Extract YouTube video ID from various URL formats.

**Supported Formats:**
- `https://www.youtube.com/watch?v=VIDEO_ID`
- `https://youtu.be/VIDEO_ID`
- `https://www.youtube.com/embed/VIDEO_ID`
- `https://www.youtube.com/v/VIDEO_ID`

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `url` | str | YouTube video URL |

**Returns:** Video ID (str) or None if invalid

**Example:**
```python
extract_video_id("https://youtu.be/dQw4w9WgXcQ")  # Returns: "dQw4w9WgXcQ"
```

#### `validate_youtube_url`

Validate a YouTube URL format.

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `url` | str | URL to validate |

**Returns:** Tuple of (is_valid: bool, error_message: str)

**Example:**
```python
is_valid, error = validate_youtube_url("https://youtu.be/abc123")
# Returns: (True, "") if valid
# Returns: (False, "Invalid YouTube URL format") if invalid
```

## Usage Example

```python
# Logging
from predictor.utils.logging_utils import get_logger

logger = get_logger(__name__)
logger.info("Starting prediction...")
logger.error("An error occurred")

# Video utilities
from predictor.utils.video_utils import extract_video_id, validate_youtube_url

# Extract video ID
video_id = extract_video_id("https://www.youtube.com/watch?v=abc123xyz")

# Validate URL
is_valid, error = validate_youtube_url("https://youtu.be/abc123xyz")
if not is_valid:
    print(f"Invalid URL: {error}")
```

## Log File Location

Log files are stored in `./logs/` directory with naming format:
```
predictor_YYYYMMDD_HHMMSS.log
```

Example: `predictor_20240115_103045.log`
