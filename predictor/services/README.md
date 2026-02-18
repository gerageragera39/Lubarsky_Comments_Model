# Services Module

## Overview

The `services` module implements the **Service layer** of the application architecture. It contains the core business logic for comment fetching and model prediction, executing in a background thread while providing real-time feedback.

## Architecture

This module follows multiple SOLID principles:
- **Single Responsibility Principle:** Each class handles a specific concern
- **Dependency Inversion Principle:** Services depend on abstractions (config objects)
- **Interface Segregation:** Clean interfaces for each component

## Files

### `__init__.py`

Package initialization file that exports service classes for external module access.

### `prediction_service.py`

**Purpose:** Implements the core prediction logic for YouTube comment classification.

**Key Classes:**

#### `YouTubeCommentFetcher`

Handles communication with YouTube API for fetching comments.

**Responsibilities:**
- Initialize YouTube API client with API key
- Fetch comments from a video with pagination
- Handle API errors gracefully
- Return list of comment texts

**Methods:**

| Method | Parameters | Returns | Description |
|--------|------------|---------|-------------|
| `__init__` | `api_key: str` | - | Initialize API client |
| `fetch_comments` | `video_id: str`, `max_results: int` | `list[str]` | Fetch comments from video |

#### `ModelPredictor`

Handles model loading and inference operations.

**Responsibilities:**
- Lazy load tokenizer and model
- Run batched inference on comment texts
- Return predictions with confidence scores
- Handle GPU/CPU device selection

**Methods:**

| Method | Parameters | Returns | Description |
|--------|------------|---------|-------------|
| `__init__` | `model_path: str` | - | Initialize predictor |
| `predict` | `texts: list[str]`, `batch_size: int` | `list[tuple[int, float]]` | Run inference |

**Properties:**

| Property | Type | Description |
|----------|------|-------------|
| `tokenizer` | AutoTokenizer | Lazy-loaded tokenizer |
| `model` | AutoModelForSequenceClassification | Lazy-loaded model |

#### `PredictionService`

Main service coordinating the prediction workflow.

**Responsibilities:**
- Coordinate comment fetching and model prediction
- Save results to CSV file
- Find trained model directories
- Provide progress callbacks

**Methods:**

| Method | Parameters | Returns | Description |
|--------|------------|---------|-------------|
| `__init__` | `api_key: str` | - | Initialize service |
| `predict` | `config: PredictionConfig`, `progress_callback: Callable` | `PredictionBatch` | Run prediction |
| `save_results` | `batch: PredictionBatch`, `output_path: str` | - | Save to CSV |
| `find_models` | `search_dir: str` | `list[str]` | Find model directories |

## Usage Example

```python
from predictor.services import PredictionService
from predictor.models import PredictionConfig

# Initialize service
service = PredictionService(api_key="your_api_key")

# Create config
config = PredictionConfig(
    model_path="./models/run_1",
    video_url="https://youtu.be/abc123",
    max_comments=100
)

# Run prediction with progress callback
def on_progress(current, total):
    print(f"Progress: {current}/{total}")

batch = service.predict(config, progress_callback=on_progress)

# Save results
service.save_results(batch, "output.csv")

# Find available models
models = service.find_models(".")
```

## Thread Safety

The `PredictionService` is designed to be used from a background thread. The `PredictionController` wraps it in a `QThread` for non-blocking GUI operation.
