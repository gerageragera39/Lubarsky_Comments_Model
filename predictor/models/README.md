# Models Module

## Overview

The `models` module implements the **Model layer** of the MVC (Model-View-Controller) architecture. It defines the data structures and configuration objects used throughout the YouTube Comment Predictor application.

## Architecture

This module follows the **Single Responsibility Principle** from SOLID design patterns. Each dataclass encapsulates a specific domain concept, ensuring clean data modeling and type safety.

## Files

### `__init__.py`

Package initialization file that exports model classes for external module access.

### `prediction_config.py`

**Purpose:** Defines data class for prediction configuration.

**Key Class:**

#### `PredictionConfig`

A dataclass that encapsulates all parameters required for comment prediction.

**Attributes:**

| Attribute | Type | Description |
|-----------|------|-------------|
| `model_path` | str | Path to the trained model directory |
| `video_url` | str | YouTube video URL to fetch comments from |
| `output_file` | str | Output CSV file path (default: "predict.csv") |
| `max_comments` | int | Maximum number of comments to fetch (default: 500) |
| `batch_size` | int | Batch size for model inference (default: 32) |

**Methods:**

| Method | Description |
|--------|-------------|
| `validate()` | Validates configuration and returns (is_valid, error_message) tuple |

### `prediction_result.py`

**Purpose:** Defines data classes for prediction results.

**Key Classes:**

#### `TargetLabel`

Enum for classification target labels.

| Value | Name | Display |
|-------|------|---------|
| `0` | `NEGATIVE` | "Negative" |
| `1` | `NEUTRAL` | "Neutral" |
| `2` | `POSITIVE` | "Positive" |

#### `PredictionResult`

Represents a single comment prediction.

**Attributes:**

| Attribute | Type | Description |
|-----------|------|-------------|
| `comment` | str | The original comment text |
| `target` | int | Predicted target class (0, 1, or 2) |
| `confidence` | float | Model confidence score (0.0 to 1.0) |

**Properties:**

| Property | Type | Description |
|----------|------|-------------|
| `target_label` | TargetLabel | Target as enum value |
| `target_display` | str | Human-readable target name |

#### `PredictionBatch`

Represents a collection of prediction results with metadata.

**Attributes:**

| Attribute | Type | Description |
|-----------|------|-------------|
| `video_url` | str | Original YouTube video URL |
| `video_id` | str | Extracted video ID |
| `results` | list[PredictionResult] | List of individual predictions |
| `total_comments` | int | Total number of comments processed |

**Properties:**

| Property | Type | Description |
|----------|------|-------------|
| `summary` | dict[str, int] | Count of predictions per label |

## Usage Example

```python
from predictor.models import PredictionConfig, PredictionResult, PredictionBatch, TargetLabel

# Create prediction config
config = PredictionConfig(
    model_path="./models/run_1",
    video_url="https://youtu.be/abc123",
    max_comments=100
)

# Validate config
is_valid, error = config.validate()

# Create prediction result
result = PredictionResult(
    comment="Great video!",
    target=2,
    confidence=0.95
)

print(result.target_display)  # "Positive"
```
